import yara
import ssdeep
import os

def analizar_malware(ruta_original, ruta_copia, ruta_regla_yara):
    print("="*60)
    print("   SIEM-READY TRIAGE: AUTOMATIZACIÓN DE YARA + SSDEEP")
    print("="*60)

    # 1. Fase de Compilación Estática (YARA)
    if not os.path.exists(ruta_regla_yara):
        print(f"[-] Error: No se localizó la regla YARA en: {ruta_regla_yara}")
        return

    print("[*] Compilando heurística de reglas estáticas...")
    rules = yara.compile(filepath=ruta_regla_yara)

    # Evaluación del binario puro original
    print(f"\n[*] Analizando flujo del espécimen original: {os.path.basename(ruta_original)}")
    if not os.path.exists(ruta_original):
        print(f"[-] ERROR: Archivo objetivo {ruta_original} no encontrado.")
    else:
        matches_original = rules.match(ruta_original)
        if matches_original:
            print(f"[+] [ ALERTA CRÍTICA ] -> POSITIVO PARA MALWARE WANNACRY")
            print(f"[>] Regla Activada: {matches_original}")
        else:
            print("[-] YARA: No se detectaron firmas estáticas coincidentes.")

    # Evaluación de la copia mutada (Para la fase posterior)
    if os.path.exists(ruta_copia):
        print(f"\n[*] Analizando flujo de la muestra mutada: {os.path.basename(ruta_copia)}")
        matches_copia = rules.match(ruta_copia)
        if matches_copia:
            print(f"[+] [ ALERTA DE EVASIÓN ] -> MUTACIÓN POSITIVA PARA WANNACRY")
            print(f"[>] Regla Activada: {matches_copia}")
        else:
            print("[-] YARA: Flujo limpio (La mutación evadió la regla estática).")
    
    print("-" * 60)

    # 2. Fase de Análisis Estructural de Contexto (SSDEEP - Fuzzy Hashing)
    print("[*] Calculando firmas de hashing difuso estructural...")
    if os.path.exists(ruta_original):
        hash_original = ssdeep.hash_from_file(ruta_original)
        print(f"[>] SSDEEP Original: {hash_original}")

        if os.path.exists(ruta_copia):
            hash_copia = ssdeep.hash_from_file(ruta_copia)
            print(f"[>] SSDEEP Mutado:   {hash_copia}")

            # Comparación algorítmica de homología entre bytes
            porcentaje_similitud = ssdeep.compare(hash_original, hash_copia)
            print("\n" + "="*60)
            print(f"[RESULTADO EVALUATIVO] Homología Estructural: {porcentaje_similitud}%")
            if porcentaje_similitud > 0:
                print("[¡WARN!] Variación detectada. Comparten bloques comunes de código.")
            else:
                print("[-] Estructuras completamente divergentes.")
            print("="*60)
        else:
            print("\n[-] Nota de control: Muestra mutada ausente. Registrando firma base de integridad.")

if __name__ == "__main__":
    # Mapeo estricto del laboratorio centrado en mayúsculas
    ORIGINAL_MALWARE = "/home/kali/Downloads/laboratorio/WannaCry.exe"
    MUTATED_MALWARE = "/home/kali/Downloads/laboratorio/wannacry_mutado.exe"
    YARA_RULESET = "/home/kali/Downloads/laboratorio/wannacry.yar"

    analizar_malware(ORIGINAL_MALWARE, MUTATED_MALWARE, YARA_RULESET)
