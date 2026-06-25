# 🔬 WannaCry Triage Toolkit

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)
![YARA](https://img.shields.io/badge/YARA-4.x-FF6B6B?style=for-the-badge&logo=virustotal&logoColor=white)
![ECS](https://img.shields.io/badge/Elastic_ECS-005571?style=for-the-badge&logo=elastic&logoColor=white)
![Status](https://img.shields.io/badge/Status-En_Desarrollo-yellow?style=for-the-badge)

**Herramienta forense de triaje de malware | YARA + SSDEEP + Entropía de Shannon**

*Desarrollada en entorno Air-Gap sobre Kali Linux | Bootcamp de Ciberseguridad Betek — Medellín, 2026*

</div>

---

## 📋 Descripción General

**WannaCry Triage Toolkit** es una herramienta de triaje forense automatizado diseñada para analizar, clasificar y correlacionar muestras de malware polimórfico en entornos de laboratorio controlados. Fue desarrollada como parte de un workshop práctico del **Bootcamp de Ciberseguridad Betek (2026)**, donde se analizó un binario real del ransomware **WannaCry** en un entorno aislado (*Air-Gap*) sobre **Kali Linux**.

La herramienta integra en un único pipeline automatizado tres tecnologías complementarias de detección:

| Tecnología | Función |
|---|---|
| **Reglas YARA** | Detección estática mediante firmas de texto plano, Unicode y patrones hexadecimales |
| **SSDEEP (Fuzzy Hashing)** | Medición de homología estructural entre variantes polimórficas (0% – 100%) |
| **Entropía de Shannon** | Detección de empaquetado/cifrado por aleatoriedad estadística de bytes |

---

## 🧪 Contexto del Laboratorio

El laboratorio fue ejecutado bajo las siguientes condiciones de seguridad:

- **Entorno**: Máquina virtual **Kali Linux 2026.1** en VMware Workstation Pro
- **Aislamiento**: Configuración *Air-Gap* con adaptador de red en modo VMnet personalizado (LAN ciega), carpetas compartidas y portapapeles deshabilitados (*Guest Isolation*)
- **Muestra analizada**: Binario real de ransomware **WannaCry** (SHA256: `3a7ad1f4cc13618fb549375990cf3cb3581eec295b852e8fc89d2032f97eeab8`) obtenido de [MalwareBazaar](https://bazaar.abuse.ch/)
- **Mutación simulada**: Modificación selectiva de bytes en el dominio del Kill-Switch (`www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`) usando **GHex** para simular polimorfismo cosmético

---

## ⚙️ Módulos Disponibles

```
╔══════════════════════════════════════════════════════════════════════╗
║          CONSOLA DE CONTROL - PROTOCOLOS DE TRIAGE                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  [01]  Triage y Análisis Masivo del Laboratorio                      ║
║  [02]  Inspección de Muestra Única (Ad-Hoc)                          ║
║  [03]  Extractor Estático de Strings e Indicadores de Red (C2)       ║
║  [04]  Análisis de Entropía de Shannon (Detección de Empaquetado)    ║
║  [05]  Auditoría y Compilación de Reglas YARA                        ║
║  [06]  Manual de Operaciones Detallado                               ║
║  [07]  Exportar Reporte de Triage a JSON (Formato SIEM/ECS)          ║
║  [08]  Salida con animación Matrix                                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Módulo 01 — Triage Masivo
Escanea un directorio completo de mutaciones. Por cada archivo genera: **SHA256**, **MD5**, **firma SSDEEP**, resultado de regla **YARA** y **porcentaje de homología** frente al binario base.

### Módulo 02 — Inspección de Muestra Única
Análisis rápido *Ad-Hoc* de un único artefacto: extrae sus hashes criptográficos completos y verifica si activa las firmas YARA cargadas.

### Módulo 03 — Extractor de Strings y C2
Analiza los bytes crudos del binario sin ejecutarlo. Busca cadenas ASCII legibles (≥ 4 caracteres) para descubrir estáticamente URLs de C2, IPs, rutas internas y funciones de la API de Windows.

### Módulo 04 — Entropía de Shannon
Aplica la fórmula matemática de Shannon sobre los bytes del archivo. Valores superiores a **7.2 / 8.0** indican cifrado o empaquetado (UPX/packers), señal de evasión de antivirus.

### Módulo 05 — Auditoría YARA
Compila el AST sintáctico del conjunto de reglas `.yar` y verifica la salud del ruleset sin ejecutar ningún análisis sobre muestras.

### Módulo 07 — Exportación JSON (ECS)
Genera un artefacto forense `triage_report.json` estructurado bajo el estándar **Elastic Common Schema (ECS)**, listo para ser ingestado por **Elasticsearch / Kibana**, **Splunk** o **Wazuh**.

---

## 📊 Resultados del Laboratorio

### Comparativa de Efectividad (Experimento WannaCry Mutado)

| Criterio | SHA-256 | YARA Estático | SSDEEP (Fuzzy) |
|---|:---:|:---:|:---:|
| Detección muestra **original** | ✅ | ✅ | ✅ |
| Detección muestra **mutada** | ❌ | ⚠️ Parcial | ✅ **99% homología** |
| Resiliencia ante polimorfismo | Nula | Moderada/Baja | **Alta** |
| Velocidad de procesamiento | Muy alta | Moderada | Moderada-Alta |
| Caso de uso óptimo en SOC | Blacklisting | Clasificación de familias | Threat Hunting |

> **Resultado clave:** La alteración selectiva de bytes en la sección Unicode del Kill-Switch anuló la firma YARA estática, pero SSDEEP mantuvo una **homología del 99%**, confirmando que ambas muestras pertenecen a la misma familia.

---

## 🚀 Instalación y Uso

### Requisitos del Sistema

- **OS**: Kali Linux 2024+ (o cualquier distribución Debian/Ubuntu)
- **Python**: 3.8 o superior
- **Dependencias del sistema**:

```bash
sudo apt update && sudo apt install yara python3-yara ssdeep python3-ssdeep libfuzzy-dev -y
```

### Estructura del Directorio Esperada

```
/home/kali/Downloads/laboratorio/
├── WannaCry.exe                  # Binario base (sin permisos de ejecución)
├── wannacry.yar                  # Reglas YARA de detección
├── analizador.py                 # Script básico del workshop
├── Kali-WannaCry-Triage-Toolkit-V0.py  # ← Esta herramienta
└── wannacry_mutaciones/
    ├── wannacry_mutado_v1.exe
    └── ...
```

### Ejecución

```bash
# Clonar el repositorio
git clone https://github.com/abrahamnaranjof/wannacry-triage-toolkit.git
cd wannacry-triage-toolkit

# Ejecutar la herramienta
python3 Kali-WannaCry-Triage-Toolkit-V0.py
```

> ⚠️ **ADVERTENCIA DE SEGURIDAD**: Esta herramienta está diseñada exclusivamente para entornos de laboratorio aislados (*Air-Gap*). Nunca ejecutar en sistemas conectados a redes de producción. Las muestras de malware deben mantenerse sin permisos de ejecución (`chmod -x WannaCry.exe`).

---

## 📁 Estructura del Repositorio

```
wannacry-triage-toolkit/
│
├── Kali-WannaCry-Triage-Toolkit-V0.py   # Script principal del toolkit
├── wannacry.yar                          # Ruleset YARA (Detector_De_WannaCry)
├── README.md                             # Este documento
│
└── docs/
    └── Workshop_Deteccion_Malware_Abraham_Naranjo.pdf
```

---

## 🛡️ Regla YARA Implementada

```yara
rule Detector_De_WannaCry {
    meta:
        Description    = "Detecta el Binario original de WannaCry mediante firmas estáticas"
        Autor_De_la_Regla_Yara = "Abraham_De_Jesús_Naranjo_Fernández"
        Fecha          = "19/Junio/2026"
    strings:
        $kill_switch = "www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com"
        $msg_bitcoin = "Please send $300 worth of bitcoin" ascii
        $exr_taskse  = "taskse.exe" ascii
        // Cabecera MZ (Portable Executable)
        $hex_mz = { 4D 5A 90 00 03 00 00 00 }
    condition:
        any of them
}
```

---

## 📚 Marco Teórico

### ¿Por qué YARA + SSDEEP?

Las **reglas YARA estáticas** son altamente efectivas contra malware conocido, pero sufren de un problema crítico: el **efecto de falso negativo ante polimorfismo**. Si un atacante altera una sola cadena del código (como el dominio del Kill-Switch), la firma deja de coincidir.

El **hashing difuso SSDEEP** (*Context Triggered Piecewise Hashing*) resuelve esto calculando el **grado de similitud estructural** entre dos archivos. A diferencia del SHA-256 (que cambia el 100% ante un solo bit modificado), SSDEEP divide el archivo en bloques contextuales y mide cuántos de esos bloques permanecen idénticos, devolviendo un porcentaje de homología.

La **integración en Python** automatiza este pipeline, permitiendo que si YARA falla pero SSDEEP devuelve >80% de similitud, el sistema genere automáticamente una alerta de **variante polimórfica**.

---

## 👨‍💻 Autor

**Abraham De Jesús Naranjo Fernández**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abraham-de-jesús-naranjo-fernández-48bb92408)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abrahamnaranjof)

- 📍 Medellín, Antioquia, Colombia
- 🎓 Bootcamp de Ciberseguridad — Betek, 2026
- 🛠️ Herramientas: Nmap · Metasploit · THC Hydra · Wireshark · Netcat · John The Ripper · YARA · SSDEEP

---

## 📖 Referencias

1. van Rossum, G., & Python Software Foundation. (2001). *The Python language reference (Version 3.x)*. https://docs.python.org/3/reference/
2. Alvarez, V. M. (2025). *YARA: The pattern matching swiss knife for malware researchers (v4.5.5)*. VirusTotal. https://virustotal.github.io/yara/
3. Kornblum, J. (2006). Identifying almost identical files using context triggered piecewise hashing. *Digital Investigation, 3*(Suppl.), 91–97. https://doi.org/10.1016/j.diin.2006.06.015
4. Kornblum, J., & ssdeep Project. (2017). *ssdeep: Fuzzy hashing program (v2.14.1)*. https://ssdeep-project.github.io/ssdeep/

---

<div align="center">

*Desarrollado con fines educativos y de investigación en ciberseguridad defensiva.*
*Bootcamp Betek — Medellín, Colombia — 2026*

</div>
