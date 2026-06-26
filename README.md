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

**WannaCry Triage Toolkit** es un script de triaje forense desarrollado como **ejercicio práctico de laboratorio** en el Workshop de Detección de Malware del **Bootcamp de Ciberseguridad Betek (2026)**. Permite analizar y comparar muestras del ransomware **WannaCry** en un entorno aislado (*Air-Gap*) sobre **Kali Linux**, integrando tres herramientas de detección en un solo flujo automatizado.

La herramienta integra en un único pipeline automatizado tres tecnologías complementarias de detección:

| Tecnología | Función |
|---|---|
| **Reglas YARA** | Detección estática mediante firmas de texto plano, Unicode y patrones hexadecimales |
| **SSDEEP (Fuzzy Hashing)** | Medición de homología estructural entre variantes polimórficas (0 % – 100 %) |
| **Entropía de Shannon** | Detección de empaquetado/cifrado por aleatoriedad estadística de bytes |

---

## 🧪 Contexto del Laboratorio

El laboratorio fue ejecutado bajo las siguientes condiciones de seguridad:

- **Entorno**: Máquina virtual **Kali Linux 2026.1** en VMware Workstation Pro
- **Aislamiento**: Configuración *Air-Gap* con adaptador de red en modo VMnet personalizado (LAN ciega), carpetas compartidas y portapapeles deshabilitados (*Guest Isolation*)
- **Muestra analizada**: Binario real de ransomware **WannaCry** obtenido de [MalwareBazaar](https://bazaar.abuse.ch/)
- **Mutación simulada**: Modificación selectiva de bytes en el dominio del Kill-Switch (`www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`) usando **GHex** para simular polimorfismo cosmético

> ⚠️ **Nota:** Verificar que el SHA256 de la muestra descargada tenga exactamente 64 caracteres hexadecimales antes de documentarlo como evidencia forense.

---

## ⚙️ Módulos Disponibles

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║     CONSOLA DE CONTROL GENERAL — PROTOCOLOS DE TRIAGE DE ARQUITECTURA DE         ║
║                              SEGURIDAD                                           ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  [01]  Ejecutar Triage y Análisis Masivo del Laboratorio                         ║
║        (Criptografía Completa + Homología)                                       ║
║  [02]  Inspección de Muestra Única Aislada                                       ║
║        (Generación de Hashes, Reglas YARA y Mapeo)                               ║
║  [03]  Extractor Estático de Strings, Buffers Ocultos e Indicadores de Red (C2)  ║
║  [04]  Análisis Estadístico de Entropía de Shannon y Detección de Empaquetado    ║
║        (Packed)                                                                  ║
║  [05]  Auditoría, Verificación de Sintaxis y Compilación de Conjuntos de         ║
║        Reglas YARA                                                               ║
║  [06]  VER MANUAL DE OPERACIONES DETALLADO                                       ║
║        (Especificaciones Técnicas del Entorno)                                   ║
║  [07]  Compilar e Ingestar Reporte de Triage a Archivo de Log JSON               ║
║        (Formato SIEM/ECS)                                                        ║
║  [08]  Destrucción de Evidencia Volátil, Limpieza Secuencial y Cierre de Sesión  ║
║        (Matrix)                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
```

### Captura — Menú principal del toolkit

![Menú principal del triaje](wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/01%20Men%C3%BA%20Principal%20Del%20Triage/Men%C3%BA.png)

---

### Módulo 01 — Triage y Análisis Masivo del Laboratorio

Escanea secuencialmente todo el directorio de mutaciones. Por cada archivo genera: **SHA256**, **MD5**, **firma SSDEEP** sin cortes, resultado de regla **YARA** y **porcentaje de homología** frente al binario base.

**Capturas de ejecución:**

![Módulo 01 — paso 1]https://github.com/abrahamnaranjof/wannacry-triage-toolkit/commit/81d02aca84ebbb5a15ba581cd5c29156713e3b50#diff-22162d1df868e70d1b93094b5ea28fad7f0203406e4618631b2ba0d99b17ca7b?raw=true
![Módulo 01 — paso 2](wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/02%20Ejecutar%20Triage%20y%20An%C3%A1lisis%20Masivo/modulo1_2.png)
![Módulo 01 — paso 3](wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/02%20Ejecutar%20Triage%20y%20An%C3%A1lisis%20Masivo/modulo1_3.png)

---

### Módulo 02 — Inspección de Muestra Única (Ad-Hoc)

Análisis rápido de un único artefacto: extrae sus hashes criptográficos completos y verifica si activa las firmas YARA cargadas. Ideal para triaje rápido de un archivo sospechoso específico sin necesidad de procesar el directorio completo.

**Capturas de ejecución:**

![Módulo 02 — paso 1](wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/03%20Inspecci%C3%B3n%20de%20Muestra%20%C3%9Anica/modulo2_1.png)
![Módulo 02 — paso 2](wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/03%20Inspecci%C3%B3n%20de%20Muestra%20%C3%9Anica/modulo2_2.png)
![Módulo 02 — paso 3](wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/03%20Inspecci%C3%B3n%20de%20Muestra%20%C3%9Anica/modulo2_3.png)

---

### Módulo 03 — Extractor Estático de Strings, Buffers Ocultos e Indicadores de Red (C2)

Analiza los bytes crudos del binario **sin ejecutarlo** (análisis estático puro). Busca cadenas ASCII legibles (≥ 4 caracteres) para descubrir estáticamente URLs de C2, IPs, rutas internas, funciones de la API de Windows y buffers ocultos.

---

### Módulo 04 — Análisis Estadístico de Entropía de Shannon (Detección de Empaquetado)

Aplica la fórmula matemática de Shannon sobre los bytes del archivo. Valores superiores a **7.2 / 8.0** indican cifrado o empaquetado (UPX / *packers*), señal de evasión de antivirus por ofuscación del *payload*.

---

### Módulo 05 — Auditoría, Verificación de Sintaxis y Compilación de Reglas YARA

Compila el AST sintáctico del conjunto de reglas `.yar` y verifica la salud del *ruleset* sin ejecutar ningún análisis sobre muestras. Detecta errores de sintaxis y conflictos entre reglas antes de desplegarlas en producción.

---

### Módulo 06 — Manual de Operaciones Detallado

Muestra las especificaciones técnicas completas del entorno: versiones de herramientas, rutas absolutas del laboratorio, dependencias del sistema y una guía de uso de cada módulo con ejemplos de salida esperada. Referencia rápida para operadores del SOC.

---

### Módulo 07 — Compilar e Ingestar Reporte de Triage a JSON (Formato SIEM/ECS)

Genera un artefacto forense `triage_report.json` estructurado bajo el estándar **Elastic Common Schema (ECS)**, listo para ser ingestado por **Elasticsearch / Kibana**, **Splunk** o **Wazuh**. Garantiza la trazabilidad y la cadena de custodia digital del análisis.

---

### Módulo 08 — Destrucción de Evidencia Volátil, Limpieza Secuencial y Cierre de Sesión (Matrix)

Cierra la sesión de forma segura mediante la **destrucción controlada de evidencia volátil**: limpia variables en memoria, buffers temporales y rastros de ejecución del toolkit. La animación Matrix actúa como confirmación visual del procedimiento de destrucción, siguiendo prácticas OPSEC para entornos Air-Gap de alta sensibilidad.

---

## 📊 Resultados del Laboratorio

### Demostración animada del toolkit en ejecución

![Demo animada del toolkit](https://github.com/abrahamnaranjof/wannacry-triage-toolkit/blob/main/wannacry-triage-toolkit/Capturas%20wannacry-triage-toolkit/00%20Demo%20De%20Herramienta%20GIF/demo_herramienta.gif?raw=true)

### Comparativa de efectividad — Experimento WannaCry Mutado

| Criterio | SHA-256 | YARA Estático | SSDEEP (Fuzzy) |
|---|:---:|:---:|:---:|
| Detección muestra **original** | ✅ | ✅ | ✅ |
| Detección muestra **mutada** | ❌ | ⚠️ Parcial | ✅ **99 % homología** |
| Resiliencia ante polimorfismo | Nula | Moderada / baja | **Alta** |
| Velocidad de procesamiento | Muy alta | Moderada | Moderada-alta |
| Caso de uso óptimo en SOC | Blacklisting | Clasificación de familias | Threat Hunting |

> **Resultado clave:** La alteración selectiva de bytes en la sección Unicode del Kill-Switch anuló la firma YARA estática, pero SSDEEP mantuvo una **homología del 99 %**, confirmando que ambas muestras pertenecen a la misma familia de malware.

---

## 🚀 Instalación y Uso

### Requisitos del sistema

- **OS**: Kali Linux 2024+ (o cualquier distribución Debian/Ubuntu)
- **Python**: 3.8 o superior
- **Dependencias del sistema**:

```bash
sudo apt update && sudo apt install yara python3-yara ssdeep python3-ssdeep libfuzzy-dev -y
```

### Estructura del directorio esperada

```
/home/kali/Downloads/laboratorio/
├── WannaCry.exe                        # Binario base (sin permisos de ejecución)
├── wannacry.yar                        # Reglas YARA de detección
├── analizador.py                       # Script básico del workshop
├── Kali-WannaCry-Triage-Toolkit-V0.py  # ← Esta es la herramienta de triaje
└── wannacry_mutaciones/                # Aquí se guardan las mutaciones para ser analizadas
    ├── wannacry_mutado_v1.exe          # Ejemplo de mutación de WannaCry.exe
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
├── Kali-WannaCry-Triage-Toolkit-V0.py    # Script principal del toolkit
├── wannacry.yar                          # Ruleset YARA (Detector_De_WannaCry)
├── README.md                             # Este documento
│
├── Capturas wannacry-triage-toolkit/     # Evidencia visual por módulo
│   ├── 00 Demo De Herramienta GIF/
│   │   └── demo_herramienta.gif
│   ├── 01 Menú Principal Del Triage/
│   │   └── Menú.png
│   ├── 02 Ejecutar Triage y Análisis Masivo/
│   │   ├── modulo1_1.png
│   │   ├── modulo1_2.png
│   │   └── modulo1_3.png
│   ├── 03 Inspección de Muestra Única/
│   │   ├── modulo2_1.png
│   │   ├── modulo2_2.png
│   │   └── modulo2_3.png
│   └── 04 Extractor Estático de Cadenas.../
│       └── ...
│
└── docs/
    └── Workshop_Deteccion_Malware_Abraham_Naranjo.pdf  # Evidencia académica previa
```

---

## 🛡️ Regla YARA Implementada

```yara
rule Detector_De_WannaCry {
    meta:
        Description             = "Detecta el Binario original de WannaCry mediante firmas estáticas"
        Autor_De_la_Regla_Yara  = "Abraham_De_Jesús_Naranjo_Fernández"
        Fecha                   = "19/Junio/2026"
    strings:
        // Kill-Switch domain (cadena Unicode — dominio de control)
        $kill_switch = "www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com"
        // Mensaje de rescate en Bitcoin
        $msg_bitcoin = "Please send $300 worth of bitcoin" ascii
        // Ejecutable interno del ransomware
        $exr_taskse  = "taskse.exe" ascii
        // Cabecera MZ (Portable Executable — formato PE)
        $hex_mz = { 4D 5A 90 00 03 00 00 00 }
    condition:
        any of them
}
```

---

## 📚 Marco Teórico

### ¿Por qué YARA + SSDEEP?

Las **reglas YARA estáticas** son altamente efectivas contra malware conocido, pero sufren de un problema crítico: el **efecto de falso negativo ante polimorfismo**. Si un atacante altera una sola cadena del código (como el dominio del Kill-Switch), la firma deja de coincidir.

El **hashing difuso SSDEEP** (*Context Triggered Piecewise Hashing*) resuelve esto calculando el **grado de similitud estructural** entre dos archivos. A diferencia del SHA-256 (que cambia completamente ante un solo bit modificado), SSDEEP divide el archivo en bloques contextuales y mide cuántos de esos bloques permanecen idénticos, devolviendo un porcentaje de homología.

La **integración en Python** automatiza este *pipeline*, permitiendo que si YARA falla pero SSDEEP devuelve > 80 % de similitud, el sistema genere automáticamente una alerta de **variante polimórfica**.

---

## 👨‍💻 Autor

**Abraham De Jesús Naranjo Fernández**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abraham-de-jesús-naranjo-fernández-48bb92408)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abrahamnaranjof)

- 📍 Medellín, Antioquia, Colombia
- 🎓 Bachiller académico con formación en Ciberseguridad — Bootcamp Betek, 2026
- 🛠️ Herramientas aprendidas en laboratorio: Nmap · Metasploit · THC Hydra · Wireshark · Netcat · John The Ripper · YARA · SSDEEP
- ⚠️ Este proyecto es un ejercicio educativo desarrollado en entorno controlado de laboratorio

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
