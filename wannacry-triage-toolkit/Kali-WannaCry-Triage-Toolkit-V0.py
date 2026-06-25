import hashlib
import math
import os
import random
import re
import sys
import time
import ssdeep
import yara
import json
from datetime import datetime, timezone

# ==============================================================================
# CONFIGURACIÓN DE COLORES (ESTÉTICA KALI-DARK)
# ==============================================================================
VERDE_NEON = "\033[1;92m"
VERDE = "\033[1;32m"
ROJO = "\033[1;31m"
AMARILLO = "\033[1;33m"
MAGENTA = "\033[1;35m"
BLANCO_BRILLANTE = "\033[1;37m"
PURPLE_CYBER = "\033[1;34m"
CYAN_BAJO = "\033[0;36m"
RESET = "\033[0m"
BORRAR_LINEA = "\033[K"


# ==============================================================================
# FUNCIONES AUXILIARES DE FORMATEO VISTA / INTERFAZ
# ==============================================================================

def calcular_longitud_real(texto_con_colores):
    """
    Remueve las secuencias de escape ANSI utilizando expresiones regulares.
    Retorna el número real de caracteres en pantalla para cálculos simétricos.
    """
    patron_ansi = re.compile(r'\x1b\[[0-9;]*m')
    texto_limpio = patron_ansi.sub('', texto_con_colores)
    return len(texto_limpio)


def ajustar_justificacion(texto, ancho, relleno=" "):
    """Alinea el texto a la izquierda rellenando de forma exacta el ancho fijo."""
    len_real = calcular_longitud_real(texto)
    faltantes = max(0, ancho - len_real)
    return texto + (relleno * faltantes)


def ejecutar_proceso_tecnico(mensaje_principal, subtareas, duracion_total=3.0):
    """Genera un indicador visual de carga realista adaptado para el triage."""
    chars_spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    pasos = len(subtareas)
    tiempo_por_paso = duracion_total / pasos
    iteraciones_por_paso = max(1, int(tiempo_por_paso / 0.18))

    contador_global = 0
    for subtarea in subtareas:
        for _ in range(iteraciones_por_paso):
            sp = chars_spinner[contador_global % len(chars_spinner)]
            sys.stdout.write(f"\r{MAGENTA}[{sp}]{RESET} {BLANCO_BRILLANTE}{mensaje_principal}...{RESET} {CYAN_BAJO}({subtarea}){RESET}{BORRAR_LINEA}")
            sys.stdout.flush()
            contador_global += 1
            time.sleep(0.18)
            
    sys.stdout.write(f"\r{VERDE_NEON}[✓] {mensaje_principal} completado de forma exitosa.{RESET}{BORRAR_LINEA}\n")
    sys.stdout.flush()
    time.sleep(0.2)


# ==============================================================================
# COMPONENTES VISUALES ANIMADOS
# ==============================================================================

def animacion_microscopio():
    """Dibuja los frames del microscopio enfocando de forma limpia la muestra."""
    subtareas_platina = [
        "Alineando lentes ópticos",
        "Estabilizando fuente de luz UV",
        "Fijando portaobjetos de seguridad",
        "Enfocando estructura de capas PE"
    ]
    ejecutar_proceso_tecnico("Montando muestras en la platina del microscopio", subtareas_platina, duracion_total=3.5)
    print("")

    # Inyectamos BORRAR_LINEA al final de cada fila para limpiar residuos horizontales
    f1 = fr"""
       {MAGENTA}||{RESET}{BORRAR_LINEA}        
    {MAGENTA} _ _||_ _{RESET}{BORRAR_LINEA}     
    {MAGENTA}(_(_||_)_){RESET}{BORRAR_LINEA}    
       {MAGENTA}||{RESET}{BORRAR_LINEA}        
       {MAGENTA}||{RESET} =====>  {AMARILLO}[ MUESTRAS COMPROMETIDAS ]{RESET}{BORRAR_LINEA}           
      {MAGENTA}/  \{RESET}{BORRAR_LINEA}
     {MAGENTA}/____\{RESET}{BORRAR_LINEA}
    """

    f2 = fr"""
       {MAGENTA}||{RESET}{BORRAR_LINEA}        
    {MAGENTA} _ _||_ _{RESET}{BORRAR_LINEA}      {MAGENTA}  .-----------------.{RESET}{BORRAR_LINEA}
    {MAGENTA}(_(_||_)_){RESET}{BORRAR_LINEA}     {MAGENTA} /  .-------------.  \{RESET}{BORRAR_LINEA}
       {MAGENTA}||{RESET}{BORRAR_LINEA}          {MAGENTA}/  /   01010110    \  \{RESET}{BORRAR_LINEA}
       {MAGENTA}||{RESET} =====>  {MAGENTA}|  |    WANNACRY     |  |{RESET}{BORRAR_LINEA}
      {MAGENTA}/  \{RESET}{BORRAR_LINEA}         {MAGENTA}\  \   11001010    /  /{RESET}{BORRAR_LINEA}
     {MAGENTA}/____\{RESET}{BORRAR_LINEA}         {MAGENTA} \  '-------------'  /{RESET}{BORRAR_LINEA}
                           {MAGENTA}'-----------------'{RESET}{BORRAR_LINEA}
    """

    f3 = fr"""
       {MAGENTA}||{RESET}{BORRAR_LINEA}        
    {MAGENTA} _ _||_ _{RESET}{BORRAR_LINEA}      {ROJO}  .-----------------.{RESET}{BORRAR_LINEA}
    {MAGENTA}(_(_||_)_){RESET}{BORRAR_LINEA}     {ROJO} /  .-------------.  \{RESET}{BORRAR_LINEA}
       {MAGENTA}||{RESET}{BORRAR_LINEA}          {ROJO}/  /  ⚠️  AMENAZA   \  \{RESET}{BORRAR_LINEA}
       {MAGENTA}||{RESET} =====>  {ROJO}|  |  CVE-2017-0143  |  |{RESET}{BORRAR_LINEA}
      {MAGENTA}/  \{RESET}{BORRAR_LINEA}         {ROJO}\  \   DETECTADA    /  /{RESET}{BORRAR_LINEA}
     {MAGENTA}/____\{RESET}{BORRAR_LINEA}         {ROJO} \  '-------------'  /{RESET}{BORRAR_LINEA}
                           {ROJO}'-----------------'{RESET}{BORRAR_LINEA}
    """

    lineas_ascii = 9
    sys.stdout.write(f1)
    sys.stdout.flush()
    time.sleep(0.8)
    sys.stdout.write(f"\033[F" * lineas_ascii)

    sys.stdout.write(f2)
    sys.stdout.flush()
    time.sleep(0.8)
    sys.stdout.write(f"\033[F" * lineas_ascii) 

    sys.stdout.write(f3)
    sys.stdout.flush()
    time.sleep(1.0)
    print("\n")


def mostrar_banner_personalizado():
    """Establece la firma corporativa de autoría."""
    banner = fr"""
{ROJO}==============================================================================================================================
{VERDE}                                    >> CREADO POR: Abraham De Jesús Naranjo Fernández <<
{ROJO}=============================================================================================================================={RESET}
    """
    print(banner)


def animacion_lluvia_matrix(duracion=3.0):
    """Despliega la caída de streams binarios emulando el núcleo Matrix."""
    try:
        columnas, filas = os.get_terminal_size()
    except OSError:
        columnas, filas = 126, 24

    caracteres = ["0", "1", "X", "Z", "§", "$", "#", "%", "&", "µ"]
    posiciones = [0] * columnas

    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < duracion:
        linea = ""
        for c in range(columnas):
            if random.random() > 0.95:
                posiciones[c] = filas
            
            if posiciones[c] > 0:
                char = random.choice(caracteres)
                color = VERDE_NEON if random.random() > 0.3 else VERDE
                linea += f"{color}{char}{RESET}"
                posiciones[c] -= 1
            else:
                linea += " "
        
        sys.stdout.write(linea + "\n")
        sys.stdout.flush()
        time.sleep(0.04)


def animacion_cierre_magico():
    """Genera la transición geométrica de limpieza terminal."""
    try:
        columnas, filas = os.get_terminal_size()
    except OSError:
        columnas, filas = 126, 24

    sys.stdout.write("\033[2J\033[H")
    for i in range(filas // 2):
        sys.stdout.write(f"\033[{i+1}H" + " " * columnas)
        sys.stdout.write(f"\033[{filas-i}H" + " " * columnas)
        sys.stdout.flush()
        time.sleep(0.02)

    centro_v = filas // 2
    centro_h = columnas // 2
    
    sys.stdout.write(f"\033[{centro_v}H" + f"{BLANCO_BRILLANTE}" + "═" * columnas + f"{RESET}")
    sys.stdout.flush()
    time.sleep(0.1)
    
    sys.stdout.write(f"\033[{centro_v}H" + " " * centro_h + f"{VERDE_NEON}✵{RESET}" + " " * centro_h)
    sys.stdout.flush()
    time.sleep(0.1)
    
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def despedida_mecanografiada_matrix():
    """Orquesta la salida cinemática imprimiendo los créditos del autor."""
    os.system('clear')
    print("\n\n")
    
    fragmentos = [
        ("Muchas gracias por usar esta herramienta creada por ", BLANCO_BRILLANTE),
        ("Abraham de Jesús Naranjo Fernández", MAGENTA),
        (" en el año de creación ", BLANCO_BRILLANTE),
        ("2026", MAGENTA),
        (".", BLANCO_BRILLANTE)
    ]
    
    sys.stdout.write(f"{VERDE_NEON}[*]{RESET} ")
    sys.stdout.flush()
    
    for texto, color in fragmentos:
        for char in texto:
            sys.stdout.write(f"{color}{char}{RESET}{VERDE_NEON}▒{RESET}")
            sys.stdout.flush()
            time.sleep(0.04)
            sys.stdout.write("\b \b")
            sys.stdout.flush()
            
    print("\n\n")
    print(f"{CYAN_BAJO}[>] Inicializando protocolo de destrucción de evidencia stager...{RESET}")
    time.sleep(1.8)


# ==============================================================================
# MÓDULOS DE COMPORTAMIENTO TÉCNICO
# ==============================================================================

def calcular_hash_archivo(ruta_archivo, algoritmo="sha256"):
    """Genera huellas criptográficas mediante procesamiento de streams binarios."""
    hash_objeto = hashlib.sha256() if algoritmo.lower() == "sha256" else hashlib.md5()
    try:
        with open(ruta_archivo, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                hash_objeto.update(bloque)
        return hash_objeto.hexdigest()
    except Exception:
        return "Error al calcular hash"


def extraer_strings_legibles(ruta_archivo, min_len=4):
    """Efectúa ingeniería estática buscando cadenas de texto imprimibles ASCII."""
    strings_encontrados = []
    try:
        with open(ruta_archivo, "rb") as f:
            contenido = f.read()
        
        current_str = ""
        for byte in contenido:
            if 32 <= byte <= 126:
                current_str += chr(byte)
            else:
                if len(current_str) >= min_len:
                    strings_encontrados.append(current_str)
                current_str = ""
        if len(current_str) >= min_len:
            strings_encontrados.append(current_str)
            
        return strings_encontrados
    except Exception as e:
        return [f"Error al leer strings: {str(e)}"]


def calcular_entropia_shannon(ruta_archivo):
    """Aplica la ecuación de Shannon para medir el desorden/compresión de bytes."""
    try:
        with open(ruta_archivo, "rb") as f:
            datos = f.read()
        
        if not datos:
            return 0.0
            
        longitud = len(datos)
        frecuencias = [0] * 256
        for byte in datos:
            frecuencias[byte] += 1
            
        entropia = 0.0
        for p in frecuencias:
            if p > 0:
                probabilidad = p / longitud
                entropia -= probabilidad * math.log2(probabilidad)
        return entropia
    except Exception:
        return -1.0


def mostrar_descripcion_modulo(titulo, explicacion):
    """Presenta la tarjeta informativa antes de iniciar operaciones."""
    os.system('clear')
    mostrar_banner_personalizado()
    
    ancho_modulo = 122
    print(f"{CYAN_BAJO}┌{'─' * (ancho_modulo - 2)}┐{RESET}")
    linea_tit = f"MÓDULO: {titulo}"
    print(f"{CYAN_BAJO}│{RESET} {ajustar_justificacion(f'{BLANCO_BRILLANTE}{linea_tit}{RESET}', ancho_modulo - 4)} {CYAN_BAJO}│{RESET}")
    print(f"{CYAN_BAJO}├{'─' * (ancho_modulo - 2)}┤{RESET}")
    
    for linea in explicacion:
        linea_comp = f"{CYAN_BAJO}*{RESET} {linea}"
        print(f"{CYAN_BAJO}│{RESET} {ajustar_justificacion(linea_comp, ancho_modulo - 4)} {CYAN_BAJO}│{RESET}")
        
    print(f"{CYAN_BAJO}└{'─' * (ancho_modulo - 2)}┘{RESET}")
    print(f"{AMARILLO}[>] Presione ENTER para inicializar la tarea operativa...{RESET}")
    input()


def desplegar_menu_principal():
    """Dibuja el dashboard optimizado a 122 columnas."""
    os.system('clear')
    mostrar_banner_personalizado()
    
    ancho_menu = 122
    c_borde = PURPLE_CYBER
    
    print(f"{c_borde}╔{'═' * (ancho_menu - 2)}╗{RESET}")
    print(f"{c_borde}║{RESET} {BLANCO_BRILLANTE}{'CONSOLA DE CONTROL GENERAL - PROTOCOLOS DE TRIAGE DE ARQUITECTURA DE SEGURIDAD'.center(ancho_menu - 4)}{RESET} {c_borde}║{RESET}")
    print(f"{c_borde}╠{'═' * (ancho_menu - 2)}╣{RESET}")
    
    opciones = [
        ("01", "Ejecutar Triage y Análisis Masivo del Laboratorio (Criptografía Completa + Homología)"),
        ("02", "Inspección de Muestra Única Isolada (Generación de Hashes, Reglas YARA y Mapeo)"),
        ("03", "Extractor Estático de Strings, Buffers Ocultos e Indicadores de Red (C2)"),
        ("04", "Análisis Estadístico de Entropía de Shannon y Detección de Empaquetamiento (Packed)"),
        ("05", "Auditoría, Verificación de Sintaxis y Compilación de Conjuntos de Reglas YARA"),
        ("06", "VER MANUAL DE OPERACIONES DETALLADO (Especificaciones Técnicas del Entorno)"),
        ("07", "Compilar e Ingestar Reporte de Triage a Archivo de Log JSON (Formato SIEM/ECS)"),
        ("08", "Destrucción de Evidencia Volátil, Limpieza Secuencial y Cierre de Sesión (Matrix)")
    ]
    
    for num, texto in opciones:
        opcion_raw = f" [{VERDE_NEON}{num}{RESET}] {texto}"
        print(f"{c_borde}║{RESET} {ajustar_justificacion(opcion_raw, ancho_menu - 4)} {c_borde}║{RESET}")
        
    print(f"{c_borde}╚{'═' * (ancho_menu - 2)}╝{RESET}")
    print("")


def desplegar_manual_detallado():
    """Despliega la documentación interactiva detallada aplicando word-wrap exacto."""
    os.system('clear')
    mostrar_banner_personalizado()
    ancho_doc = 110
    c_borde = CYAN_BAJO
    
    print(f"{c_borde}╔{'═' * (ancho_doc - 2)}╗{RESET}")
    print(f"{c_borde}║{RESET} {BLANCO_BRILLANTE}{'MANUAL DE ESPECIFICACIONES TÉCNICAS DEL FRAMEWORK'.center(ancho_doc - 4)}{RESET} {c_borde}║{RESET}")
    print(f"{c_borde}╠{'═' * (ancho_doc - 2)}╣{RESET}")
    
    manual_data = [
        ("MÓDULO 01 - TRIAGE Y ANÁLISIS MASIVO DE LA DIRECCIÓN", 
         ["Finalidad: Automatiza el triage forense en lote sobre directorios de malware mutado o variantes polimórficas.",
          "Mecanismo técnico: Aplica haseado criptográfico en paralelo (MD5 y SHA256) complementado con Hash de Similitud Fuzzy (SSDEEP) y escaneo heurístico YARA. Cruza cada mutación con el binario base para mapear la evolución del ataque."]),
        
        ("MÓDULO 02 - INSPECCIÓN DE MUESTRA ÚNICA (AD-HOC)", 
         ["Finalidad: Aislar un único artefacto del disco para análisis rápido sin comprometer rendimiento masivo.",
          "Mecanismo técnico: Mapea las cabeceras lógicas primarias del binario, extrayendo su huella SHA256 para cruce en bases de IOCs (Threat Intelligence) y ejecutando un motor de firmas estricto YARA sobre la muestra."]),
        
        ("MÓDULO 03 - EXTRACTOR DE STRINGS E INDICADORES DE RED (C2)", 
         ["Finalidad: Identificar propiedades estáticas del malware como direcciones IP, dominios Command & Control o llamadas API.",
          "Mecanismo técnico: Realiza un volcado lineal de bytes buscando buffers continuos legibles en formato ASCII/Unicode de longitud >= 4. Útil para extraer variables de configuración cableadas (Hardcoded) sin detonar el binario."]),
        
        ("MÓDULO 04 - ENTROPÍA DE SHANNON Y DETECCIÓN DE PACKED", 
         ["Finalidad: Determinar científicamente si un binario sospechoso se encuentra comprimido, empaquetado u ofuscado.",
          "Mecanismo técnico: Calcula la tasa de aleatoriedad de bytes en escala logarítmica de 0 a 8. Un binario plano suele marcar menor a 6.0; puntuaciones superiores a 7.2 revelan el uso de packers (UPX, Themida) para evadir firmas estáticas."]),
        
        ("MÓDULO 05 - AUDITORÍA Y COMPILACIÓN YARA", 
         ["Finalidad: Control de calidad del set de firmas heurísticas e indicadores lógicos.",
          "Mecanismo técnico: Valida la gramática, construcciones lógicas de texto y comodines del archivo de reglas (.yar), compilando el Árbol de Sintaxis Abstracta (AST) para asegurar el rendimiento en tiempo de ejecución masivo."]),

        ("MÓDULO 06 - DESPLIEGUE INTERACTIVO DEL MANUAL", 
         ["Finalidad: Proporcionar documentación de referencia inmediata directamente en la consola de Kali Linux.",
          "Mecanismo técnico: Renderiza estructuras tubulares formateadas dinámicamente en tiempo de ejecución calculando la longitud de strings en pantalla mediante la supresión lógica de bytes de color ANSI."]),

        ("MÓDULO 07 - VOLCADO FORENSE SILENCIOSO (JSON - ECS)", 
         ["Finalidad: Generación limpia de artefactos de auditoría de seguridad legibles por máquinas sin ruido visual.",
          "Mecanismo técnico: Mapea directorios enteros, extrayendo metadatos criptográficos completos sin truncamiento. Normaliza la salida bajo el estándar Elastic Common Schema (ECS) para su ingesta directa en ELK Stack o Splunk."])
    ]
    
    ancho_util = ancho_doc - 6  # Espacio interno real libre para el texto
    
    for titulo, bloques_texto in manual_data:
        # Título formateado con su color original
        tit_coloreado = f"{VERDE_NEON}{titulo}{RESET}"
        espacio_tit = ancho_util + 2 - calcular_longitud_real(tit_coloreado)
        print(f"{c_borde}║{RESET}  {tit_coloreado}{' ' * espacio_tit}{c_borde}║{RESET}")
        print(f"{c_borde}║{' ' * (ancho_doc - 2)}║{RESET}")
        
        for parrafo in bloques_texto:
            # Añadir viñeta al inicio de cada bloque conceptual
            texto_procesar = f"• {parrafo}"
            
            # Divide el texto automáticamente si excede el ancho útil asignado
            palabras = texto_procesar.split(' ')
            linea_actual = ""
            
            for palabra in palabras:
                if len(linea_actual + palabra) + 1 <= ancho_util:
                    linea_actual += (palabra + " ")
                else:
                    espacio_relleno = (ancho_doc - 4) - len(linea_actual.strip())
                    print(f"{c_borde}║{RESET}  {BLANCO_BRILLANTE}{linea_actual.strip()}{RESET}{' ' * espacio_relleno}{c_borde}║{RESET}")
                    linea_actual = palabra + " "
            
            if linea_actual:
                espacio_relleno = (ancho_doc - 4) - len(linea_actual.strip())
                print(f"{c_borde}║{RESET}  {BLANCO_BRILLANTE}{linea_actual.strip()}{RESET}{' ' * espacio_relleno}{c_borde}║{RESET}")
        
        # Separador interno estilizado entre módulos
        if titulo != manual_data[-1][0]:
            print(f"{c_borde}╠{'─' * (ancho_doc - 2)}╣{RESET}")
            
    print(f"{c_borde}╚{'═' * (ancho_doc - 2)}╝{RESET}\n")


def ejecutar_modulo_strings(ruta_defecto):
    """Módulo operativo para la extracción de buffers ASCII legibles."""
    print(f"\n{PURPLE_CYBER}[*] Configuración del extractor de texto binario.{RESET}")
    print(f"{AMARILLO}[INFO] Presione ENTER para usar la muestra por defecto ({os.path.basename(ruta_defecto)}){RESET}")
    ruta_archivo = input(f"{BLANCO_BRILLANTE}  Ruta del binario: {RESET}").strip()
    if not ruta_archivo:
        ruta_archivo = ruta_defecto
        
    if not os.path.exists(ruta_archivo) or not os.path.isfile(ruta_archivo):
        print(f"{ROJO}[- ERROR] Archivo inválido.{RESET}")
        return
        
    subtareas = ["Escaneando mapas de bytes", "Filtrando rangos ASCII legibles"]
    ejecutar_proceso_tecnico("Extrayendo cadenas ocultas", subtareas, duracion_total=2.5)
    
    lista_strings = extraer_strings_legibles(ruta_archivo)
    
    ancho_caja = 122
    print(f"\n{MAGENTA}┌{'─' * (ancho_caja - 2)}┐{RESET}")
    titulo_caja = f"{BLANCO_BRILLANTE}MUESTRA DE STRINGS IDENTIFICADOS (TOP 20){RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(titulo_caja, ancho_caja - 4)} {MAGENTA}│{RESET}")
    print(f"{MAGENTA}├{'─' * (ancho_caja - 2)}┤{RESET}")
    
    for s in lista_strings[:20]:
        s_limpio = s[:110] + "..." if len(s) > 110 else s
        linea_str = f" {CYAN_BAJO}•{RESET} {s_limpio}"
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion(linea_str, ancho_caja - 4)} {MAGENTA}│{RESET}")
        
    print(f"{MAGENTA}└{'─' * (ancho_caja - 2)}┘{RESET}")
    print(f"{VERDE_NEON}[✓] Extracción terminada. Total extraídos: {len(lista_strings)}{RESET}")


def ejecutar_modulo_entropia(ruta_defecto):
    """Módulo evaluador del grado de entropía."""
    print(f"\n{PURPLE_CYBER}[*] Configuración del analizador de aleatoriedad.{RESET}")
    print(f"{AMARILLO}[INFO] Presione ENTER para usar la muestra por defecto ({os.path.basename(ruta_defecto)}){RESET}")
    ruta_archivo = input(f"{BLANCO_BRILLANTE}  Ruta del binario: {RESET}").strip()
    if not ruta_archivo:
        ruta_archivo = ruta_defecto
        
    if not os.path.exists(ruta_archivo) or not os.path.isfile(ruta_archivo):
        print(f"{ROJO}[- ERROR] Archivo inválido.{RESET}")
        return
        
    subtareas = ["Contabilizando ocurrencias de bytes", "Aplicando fórmula estadística"]
    ejecutar_proceso_tecnico("Midiendo entropía matemática", subtareas, duracion_total=2.5)
    
    h = calcular_entropia_shannon(ruta_archivo)
    
    ancho_caja = 122
    print(f"\n{MAGENTA}┌{'─' * (ancho_caja - 2)}┐{RESET}")
    
    linea_puntaje = f"{PURPLE_CYBER}PUNTUACIÓN DE ENTROPÍA:{RESET} {BLANCO_BRILLANTE}{h:.4f} / 8.0000{RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(linea_puntaje, ancho_caja - 4)} {MAGENTA}│{RESET}")
    
    if h > 7.2:
        diag = f"{PURPLE_CYBER}DIAGNÓSTICO:{RESET} {ROJO}ALTA ENTROPÍA (Posible Packed/Encriptado){RESET}"
        alerta = f"{AMARILLO}[!] Alerta: El malware usa empaquetadores avanzados.{RESET}"
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion(diag, ancho_caja - 4)} {MAGENTA}│{RESET}")
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion(alerta, ancho_caja - 4)} {MAGENTA}│{RESET}")
    else:
        diag = f"{PURPLE_CYBER}DIAGNÓSTICO:{RESET} {VERDE}Entropía normal (Código expuesto/Legible){RESET}"
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion(diag, ancho_caja - 4)} {MAGENTA}│{RESET}")
        
    print(f"{MAGENTA}└{'─' * (ancho_caja - 2)}┘{RESET}")


def auditoria_yara(ruta_regla_yara):
    """Valida la sintaxis del motor de firmas heurísticas."""
    print(f"\n{PURPLE_CYBER}[*] Iniciando verificación de firmas...{RESET}\n")
    if not os.path.exists(ruta_regla_yara):
        print(f"{ROJO}[- ] Error: Archivo YARA ausente en: {ruta_regla_yara}{RESET}")
        return
    try:
        rules = yara.compile(filepath=ruta_regla_yara)
        count = sum(1 for _ in rules)
        print(f"{VERDE_NEON}[✓] Reglas compiladas con éxito.{RESET} Total de firmas cargadas: {BLANCO_BRILLANTE}{count}{RESET}")
    except Exception as e:
        print(f"{ROJO}[- ] Error en sintaxis YARA: {str(e)}{RESET}")


def inspeccionar_muestra_unica(ruta_defecto, ruta_regla_yara):
    """Inspección ad-hoc focalizada sobre un vector comprometido."""
    print(f"\n{PURPLE_CYBER}[*] Configuración de inspección atómica.{RESET}")
    print(f"{AMARILLO}[INFO] Presione ENTER directamente para usar la muestra por defecto ({os.path.basename(ruta_defecto)}){RESET}")
    ruta_archivo = input(f"{BLANCO_BRILLANTE}  Ingrese la ruta exacta del binario: {RESET}").strip()
    
    if not ruta_archivo:
        ruta_archivo = ruta_defecto
    
    if not os.path.exists(ruta_archivo) or not os.path.isfile(ruta_archivo):
        print(f"{ROJO}[- ERROR] Archivo no localizado o inválido en: {ruta_archivo}{RESET}")
        return

    subtareas_analisis = ["Leyendo cabeceras PE", "Haseando bloques", "Cruzando firmas YARA"]
    ejecutar_proceso_tecnico("Analizando espécimen aislado", subtareas_analisis, duracion_total=2.8)
    
    sha256_m = calcular_hash_archivo(ruta_archivo, "sha256")
    ssdeep_m = ssdeep.hash_from_file(ruta_archivo)
    
    rules = yara.compile(filepath=ruta_regla_yara)
    matches = rules.match(ruta_archivo)
    
    resultado_yara_plano = "POSITIVO" if matches else "LIMPIO"
    color_yara = ROJO if matches else VERDE
    
    ancho_caja = 122
    print(f"\n{MAGENTA}┌{'─' * (ancho_caja - 2)}┐{RESET}")
    titulo_seccion = f"{BLANCO_BRILLANTE}RESULTADOS DE EXTRACCIÓN RÁPIDA (MUESTRA ÚNICA){RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(titulo_seccion, ancho_caja - 4)} {MAGENTA}│{RESET}")
    print(f"{MAGENTA}├{'─' * (ancho_caja - 2)}┤{RESET}")
    
    l_sha = f"{PURPLE_CYBER}SHA256:{RESET} {BLANCO_BRILLANTE}{sha256_m}{RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(l_sha, ancho_caja - 4)} {MAGENTA}│{RESET}")
    
    l_ssdeep = f"{PURPLE_CYBER}SSDEEP:{RESET} {CYAN_BAJO}{ssdeep_m}{RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(l_ssdeep, ancho_caja - 4)} {MAGENTA}│{RESET}")
    
    l_yara = f"{PURPLE_CYBER}ESTADO YARA:{RESET} {color_yara}{resultado_yara_plano}{RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(l_yara, ancho_caja - 4)} {MAGENTA}│{RESET}")
    
    print(f"{MAGENTA}└{'─' * (ancho_caja - 2)}┘{RESET}")


def exportar_log_json_ecs(lista_registros, ruta_salida):
    """
    Transforma la lista de diccionarios capturada durante el análisis masivo
    en un archivo .json estructurado bajo el formato ECS (Elastic Common Schema).
    """
    envoltura_siem = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": {
            "name": "Kali-WannaCry-Triage-Toolkit",
            "version": "1.0-build2026",
            "author": "Abraham De Jesús Naranjo Fernández"
        },
        "event": {
            "kind": "event",
            "category": ["malware", "file_analysis"],
            "type": ["info"]
        },
        "summary": {
            "total_files_scanned": len(lista_registros)
        },
        "threat_reports": lista_registros
    }

    try:
        with open(ruta_salida, "w", encoding="utf-8") as archivo_log:
            json.dump(envoltura_siem, archivo_log, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"\n{ROJO}[- ERROR I/O] Falló la escritura del artefacto de log: {str(e)}{RESET}")
        return False


def ejecutar_triage_completo(ruta_base, carpeta_mutaciones, ruta_regla_yara):
    """Módulo de Triage Masivo con renders completos y sin truncación."""
    animacion_microscopio()

    subtareas_crypto = [
        "Unificando buffers criptográficos",
        "Mapeando vectores de entropía binaria",
        "Compilando AST de reglas dinámicas YARA",
        "Estructurando matriz de hashes"
    ]
    ejecutar_proceso_tecnico("Compilando matriz criptográfica y escaneando heurística", subtareas_crypto, duracion_total=3.5)
    print("")

    if not os.path.exists(ruta_regla_yara):
        print(f"{ROJO}[- ] Error: No se localizó la regla YARA en: {ruta_regla_yara}{RESET}")
        return

    rules = yara.compile(filepath=ruta_regla_yara)
    hash_base_ssdeep = ssdeep.hash_from_file(ruta_base) if os.path.exists(ruta_base) else ""

    if not hash_base_ssdeep or not os.path.exists(carpeta_mutaciones):
        print(f"{ROJO}[- ERROR] Verifique las rutas del laboratorio base.")
        return

    archivos_a_procesar = [
        os.path.join(carpeta_mutaciones, f)
        for f in os.listdir(carpeta_mutaciones)
        if os.path.isfile(os.path.join(carpeta_mutaciones, f))
    ]
    archivos_a_procesar.sort()

    memoria_recoleccion_logs = []

    ancho_col1 = 24
    ancho_col2 = 96
    
    linea_superior = "┌" + "─" * (ancho_col1 + 2) + "┬" + "─" * (ancho_col2 + 2) + "┐"
    linea_division = "├" + "─" * (ancho_col1 + 2) + "┼" + "─" * (ancho_col2 + 2) + "┤"
    linea_inferior = "└" + "─" * (ancho_col1 + 2) + "┴" + "─" * (ancho_col2 + 2) + "┘"
    
    print(f"{MAGENTA}{linea_superior}{RESET}")
    tit_col1 = f"{BLANCO_BRILLANTE}OBJETIVO DE ANÁLISIS{RESET}"
    tit_col2 = f"{BLANCO_BRILLANTE}IDENTIFICADORES INTEGRALES COMPLETOS / MATRIZ DE SIMILITUD DIRECTA{RESET}"
    print(f"{MAGENTA}│{RESET} {ajustar_justificacion(tit_col1, ancho_col1)} {MAGENTA}│{RESET} {ajustar_justificacion(tit_col2, ancho_col2)} {MAGENTA}│{RESET}")
    print(f"{MAGENTA}{linea_division}{RESET}")

    for idx, ruta_muestra in enumerate(archivos_a_procesar):
        nombre_archivo = os.path.basename(ruta_muestra)
        nombre_archivo_formateado_pantalla = nombre_archivo[:ancho_col1-3] + "..." if len(nombre_archivo) > ancho_col1 else nombre_archivo
        
        sha256_m = calcular_hash_archivo(ruta_muestra, "sha256")
        md5_m = calcular_hash_archivo(ruta_muestra, "md5")
        ssdeep_m = ssdeep.hash_from_file(ruta_muestra)
        
        similitud = ssdeep.compare(hash_base_ssdeep, ssdeep_m)
        matches = rules.match(ruta_muestra)
        
        registro_espécimen = {
            "file": {
                "name": nombre_archivo,
                "path": ruta_muestra,
                "hash": {
                    "sha256": sha256_m,
                    "md5": md5_m,
                    "ssdeep": ssdeep_m
                }
            },
            "threat_intel": {
                "yara_detection": bool(matches),
                "rule_matched": "WannaCry_Ransomware" if matches else "None",
                "fuzzy_similarity_percentage": similitud
            }
        }
        memoria_recoleccion_logs.append(registro_espécimen)

        resultado_yara = "POSITIVO (Wannacry)" if matches else "Limpio"
        color_yara = ROJO if matches else VERDE
        color_porcentaje = VERDE_NEON if similitud > 50 else AMARILLO

        l_sha = f"{PURPLE_CYBER}SHA256:{RESET} {BLANCO_BRILLANTE}{sha256_m}{RESET}"
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion(f'{BLANCO_BRILLANTE}{nombre_archivo_formateado_pantalla}{RESET}', ancho_col1)} {MAGENTA}│{RESET} {ajustar_justificacion(l_sha, ancho_col2)} {MAGENTA}│{RESET}")
        
        l_md5 = f"{PURPLE_CYBER}MD5:{RESET}    {BLANCO_BRILLANTE}{md5_m}{RESET}"
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion('', ancho_col1)} {MAGENTA}│{RESET} {ajustar_justificacion(l_md5, ancho_col2)} {MAGENTA}│{RESET}")
        
        l_ssdeep = f"{PURPLE_CYBER}SSDEEP:{RESET} {CYAN_BAJO}{ssdeep_m}{RESET}"
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion('', ancho_col1)} {MAGENTA}│{RESET} {ajustar_justificacion(l_ssdeep, ancho_col2)} {MAGENTA}│{RESET}")
        
        l_extra = f"{PURPLE_CYBER}YARA:{RESET}   {color_yara}{resultado_yara}{RESET}"
        l_homo = f"{PURPLE_CYBER}HOMOLOGÍA:{RESET} {color_porcentaje}{similitud}%{RESET}"
        
        espacios_en_medio = ancho_col2 - (calcular_longitud_real(l_extra) + calcular_longitud_real(l_homo))
        l_final_col2 = l_extra + (" " * max(0, espacios_en_medio)) + l_homo
        
        print(f"{MAGENTA}│{RESET} {ajustar_justificacion('', ancho_col1)} {MAGENTA}│{RESET} {l_final_col2} {MAGENTA}│{RESET}")

        if idx < len(archivos_a_procesar) - 1:
            print(f"{MAGENTA}{linea_division}{RESET}")
        time.sleep(0.12)

    print(f"{MAGENTA}{linea_inferior}{RESET}")
    
    subtareas_reporte = ["Estructurando JSON bajo norma ECS", "Validando firmas", "Volcando buffer al disco"]
    ejecutar_proceso_tecnico("Compilando reporte estructurado de auditoría", subtareas_reporte, duracion_total=2.0)
    
    ruta_archivo_log = os.path.join(os.path.dirname(carpeta_mutaciones), "triage_report.json")
    log_creado_con_exito = exportar_log_json_ecs(memoria_recoleccion_logs, ruta_archivo_log)

    if log_creado_con_exito:
        print(f"\n{VERDE_NEON}[✓] Artefacto forense JSON generado correctamente en:{RESET}")
        print(f"    └── {BLANCO_BRILLANTE}{ruta_archivo_log}{RESET}")
    else:
        print(f"\n{ROJO}[!] Advertencia: El reporte en pantalla finalizó, pero no se pudo volcar el JSON.{RESET}")

    print(f"\n{VERDE_NEON}[✓] Análisis del directorio masivo finalizado de forma correcta.{RESET}")

def ejecutar_triage_silencioso(ruta_base, carpeta_mutaciones, ruta_regla_yara):
    """Módulo de Triage Silencioso para la compilación directa de logs sin renderizado interactivo."""
    if not os.path.exists(ruta_regla_yara):
        print(f"{ROJO}[- ] Error: No se localizó la regla YARA en: {ruta_regla_yara}{RESET}")
        return

    try:
        rules = yara.compile(filepath=ruta_regla_yara)
    except Exception as e:
        print(f"{ROJO}[- ] Error en sintaxis YARA: {str(e)}{RESET}")
        return

    hash_base_ssdeep = ssdeep.hash_from_file(ruta_base) if os.path.exists(ruta_base) else ""

    if not hash_base_ssdeep or not os.path.exists(carpeta_mutaciones):
        print(f"{ROJO}[- ERROR] Verifique las rutas del laboratorio base.{RESET}")
        return

    archivos_a_procesar = [
        os.path.join(carpeta_mutaciones, f)
        for f in os.listdir(carpeta_mutaciones)
        if os.path.isfile(os.path.join(carpeta_mutaciones, f))
    ]
    archivos_a_procesar.sort()

    memoria_recoleccion_logs = []

    subtareas_silenciosas = [
        "Mapeando índices de archivos mutados",
        "Calculando hashes criptográficos en background",
        "Evaluando firmas heurísticas sin salida de consola",
        "Estructurando objetos bajo el estándar ECS"
    ]
    ejecutar_proceso_tecnico("Ejecutando recolección automatizada de logs", subtareas_silenciosas, duracion_total=2.0)

    for ruta_muestra in archivos_a_procesar:
        nombre_archivo = os.path.basename(ruta_muestra)
        
        sha256_m = calcular_hash_archivo(ruta_muestra, "sha256")
        md5_m = calcular_hash_archivo(ruta_muestra, "md5")
        ssdeep_m = ssdeep.hash_from_file(ruta_muestra)
        
        similitud = ssdeep.compare(hash_base_ssdeep, ssdeep_m)
        matches = rules.match(ruta_muestra)
        
        registro_especimen = {
            "file": {
                "name": nombre_archivo,
                "path": ruta_muestra,
                "hash": {
                    "sha256": sha256_m,
                    "md5": md5_m,
                    "ssdeep": ssdeep_m
                }
            },
            "threat_intel": {
                "yara_detection": bool(matches),
                "rule_matched": "WannaCry_Ransomware" if matches else "None",
                "fuzzy_similarity_percentage": similitud
            }
        }
        memoria_recoleccion_logs.append(registro_especimen)

    ruta_archivo_log = os.path.join(os.path.dirname(carpeta_mutaciones), "triage_report.json")
    log_creado_con_exito = exportar_log_json_ecs(memoria_recoleccion_logs, ruta_archivo_log)

    if log_creado_con_exito:
        print(f"\n{VERDE_NEON}[✓] Artefacto forense JSON generado correctamente en:{RESET}")
        print(f"    └── {BLANCO_BRILLANTE}{ruta_archivo_log}{RESET}")
    else:
        print(f"\n{ROJO}[!] Advertencia: No se pudo volcar el JSON de auditoría en el disco.{RESET}")

    print(f"\n{VERDE_NEON}[✓] Triage silencioso completado de forma exitosa.{RESET}")

# ==============================================================================
# ORQUESTADOR CENTRAL (MAIN)
# ==============================================================================

def main():
    """Lazo de ejecución primordial."""
    BASE_DIR = "/home/kali/Downloads/laboratorio"
    ORIGINAL_MALWARE = os.path.join(BASE_DIR, "WannaCry.exe")
    MUTATIONS_DIR = os.path.join(BASE_DIR, "wannacry_mutaciones")
    YARA_RULESET = os.path.join(BASE_DIR, "wannacry.yar")

    while True:
        desplegar_menu_principal()
        sys.stdout.write(f"{MAGENTA}[?]{RESET} {BLANCO_BRILLANTE}Seleccione un módulo de ejecución (1-8): {RESET}")
        sys.stdout.flush()
        opcion = input().strip()
        
        if opcion == "1":
            mostrar_descripcion_modulo(
                "Triage y Análisis Masivo del Laboratorio",
                [
                    "Monta las muestras en el microscopio ASCII limpio de caracteres huérfanos.",
                    "Escanea de forma secuencial todo el directorio de mutaciones.",
                    "Genera una matriz comparativa con identificadores extendidos (SHA256, MD5 y SSDEEP sin cortes).",
                    "Aplica reglas YARA y calcula porcentajes exactos de homología por similitud difusa."
                ]
            )
            ejecutar_triage_completo(ORIGINAL_MALWARE, MUTATIONS_DIR, YARA_RULESET)
            input(f"\n{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "2":
            mostrar_descripcion_modulo(
                "Inspección de Muestra Única",
                [
                    "Permite aislar un solo archivo sospechoso del disco.",
                    "Extrae sus identificadores criptográficos completos en tiempo real a ancho extendido.",
                    "Verifica si el binario activa las firmas YARA cargadas.",
                    "Es ideal para análisis rápidos dirigidos (Ad-Hoc)."
                ]
            )
            inspeccionar_muestra_unica(ORIGINAL_MALWARE, YARA_RULESET)
            input(f"\n{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "3":
            mostrar_descripcion_modulo(
                "Extractor de Strings e Indicadores de Red (C2)",
                [
                    "Analiza los bytes crudos del archivo sin ejecutarlo.",
                    "Busca secuencias de caracteres legibles (ASCII >= 4 chars).",
                    "Permite descubrir de forma estática IPs, dominios de atacantes,",
                    "funciones de la API de Windows comprometidas o rutas internas."
                ]
            )
            ejecutar_modulo_strings(ORIGINAL_MALWARE)
            input(f"\n{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "4":
            mostrar_descripcion_modulo(
                "Cálculo de Entropía y Detección de Empaquetado",
                [
                    "Mide matemáticamente la aleatoriedad de los bytes del archivo.",
                    "Utiliza la fórmula de Shannon arrojando un puntaje de 0 a 8.",
                    "Si el puntaje supera 7.2, indica de forma científica que",
                    "el malware está encriptado o empaquetado (UPX) para evadir AV."
                ]
            )
            ejecutar_modulo_entropia(ORIGINAL_MALWARE)
            input(f"\n{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "5":
            mostrar_descripcion_modulo(
                "Auditoría de Firmas y Compilación YARA",
                [
                    "Comprueba el estado de salud de tus conjuntos de reglas (.yar).",
                    "Compila el AST sintáctico para asegurar que no contenga errores.",
                    "Indica el número total de firmas que están operativas en el motor."
                ]
            )
            auditoria_yara(YARA_RULESET)
            input(f"\n{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "6":
            desplegar_manual_detallado()
            input(f"{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "7":
            mostrar_descripcion_modulo(
                "Compilación y Volcado de Artefactos de Log (JSON)",
                [
                    "Ejecuta un escaneo silencioso sobre el directorio de mutaciones.",
                    "Captura todos los hashes (MD5, SHA256, SSDEEP) sin truncar.",
                    "Estructura el output bajo la norma Elastic Common Schema (ECS).",
                    "Genera el archivo 'triage_report.json' listo para ser consumido",
                    "por motores de indexación como Splunk, ELK Stack o Wazuh."
                ]
            )
            ejecutar_triage_silencioso(ORIGINAL_MALWARE, MUTATIONS_DIR, YARA_RULESET)
            input(f"\n{AMARILLO}[ Presione ENTER para volver al menú principal ]{RESET}")
            
        elif opcion == "8":
            despedida_mecanografiada_matrix()
            animacion_lluvia_matrix(duracion=3.0)
            animacion_cierre_magico()
            print(f"{PURPLE_CYBER}[ CONEXIÓN TERMINADA - COMPORTAMIENTO SEGURO ]{RESET}\n")
            break

        else:
            print(f"{ROJO}[!] Módulo inválido. Intente de nuevo.{RESET}")
            time.sleep(1.0)

if __name__ == "__main__":
    main()
