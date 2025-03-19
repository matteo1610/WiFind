# WIFISNIFFER
# python3 wifi_sniffer_linux.py
# Raccoglie segnali wifi presenti in zona ad intervalli regolari di tempo.
# Out: file csv con i dati raccolti

import subprocess
import re
import csv
import time
from datetime import datetime

def scan_wifi():
    """Esegue la scansione delle reti Wi-Fi e restituisce una lista di dizionari con BSSID, SSID e segnale."""
    try:
        result = subprocess.run(["sudo", "iw", "dev", "wlo1", "scan"], capture_output=True, text=True)
        output = result.stdout
    except Exception as e:
        print(f"Errore durante l'esecuzione del comando: {e}")
        return []
    
    networks = []
    current_bssid = None
    current_signal = None
    current_ssid = None
    
    for line in output.split("\n"):
        line = line.strip()
        bssid_match = re.match(r'BSS ([0-9a-fA-F:]+)', line)
        signal_match = re.match(r'signal: (-?\d+\.\d+) dBm', line)
        ssid_match = re.match(r'SSID: (.+)', line)
        
        if bssid_match:
            if current_bssid and current_ssid and current_signal:
                networks.append({
                    "BSSID": current_bssid,
                    "SSID": current_ssid,
                    "Signal": float(current_signal)
                })
            current_bssid = bssid_match.group(1)
            current_signal = None
            current_ssid = None
        elif signal_match:
            current_signal = signal_match.group(1)
        elif ssid_match:
            current_ssid = ssid_match.group(1)
    
    if current_bssid and current_ssid and current_signal:
        networks.append({
            "BSSID": current_bssid,
            "SSID": current_ssid,
            "Signal": float(current_signal)
        })
    
    return networks

def save_to_csv(data, filename="wifi_scan.csv", aula="", situazione=""):
    """Salva i dati Wi-Fi in un file CSV."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Timestamp", "Aula", "Situazione", "BSSID", "SSID", "Signal"])
        if file.tell() == 0:
            writer.writeheader()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for row in data:
            row.update({"Timestamp": timestamp, "Aula": aula, "Situazione": situazione})
            writer.writerow(row)
    print(f"Dati salvati in {filename}")

def main():
    """Esegue la scansione in loop con un delay di 3 secondi e salva i dati."""
    aula = input("Inserisci l'aula: ")
    situazione = input("Inserisci la situazione (empty o crowded): ")
    count = 0
    
    try:
        while True:
            print(f"Eseguendo scansione numero {count+1}...")
            wifi_data = scan_wifi()
            if wifi_data:
                save_to_csv(wifi_data, aula=aula, situazione=situazione)
            else:
                print("Nessuna rete rilevata.")
            count += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterruzione del programma da parte dell'utente.")
    
if __name__ == "__main__":
    main()
