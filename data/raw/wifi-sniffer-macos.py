import subprocess
import time
import csv
import re
import os

"""
Wi-Fi Sniffer for macOS

This script collects information about available Wi-Fi networks using `system_profiler SPAirPortDataType` and saves it to a CSV file.

Usage:
- Run: `python3 sniffer.py`
- Enter the current location (e.g., "Room 101", "Library")
- Press ENTER for each new scan
- Stop with CTRL+C

Collected data:
- **Timestamp**: date and time of the scan
- **Location**: user-entered location
- **SSID**: Wi-Fi network name
- **Channel**: Wi-Fi channel number
- **Security**: network security type
- **RSSI**: Wi-Fi signal strength
- **Band**: 2.4GHz or 5GHz
"""

# CSV file name to store the data
csv_file = "wifi_data.csv"

# Ensure the file exists and has a header
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Location", "SSID", "Channel", "Security", "RSSI", "Band", "Status"])

# Ask the user for the current location (e.g., "Room 101", "Library")
location = input("Enter the current location (e.g., Room 101, Library): ")
status = input("Enter the status (e.g., empty, hybrid, crowded): ")
counter = 0

# Open the CSV file for appending data
with open(csv_file, "a", newline="") as file:
    writer = csv.writer(file)
    
    try:
        while True:
            # input("Press ENTER to start a new scan...")
            # Get the timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Run the command to get Wi-Fi data
            result = subprocess.run(["system_profiler", "SPAirPortDataType"], capture_output=True, text=True)
            lines = result.stdout.split("\n")

            # Flag to identify available Wi-Fi networks
            parsing_networks = False
            ssid, channel, security, rssi, band = "", "", "", "", ""

            for line in lines:
                line = line.strip()

                # Start reading available Wi-Fi networks
                if "Other Local Wi-Fi Networks:" in line:
                    parsing_networks = True
                    continue

                # Extract data if reading networks
                if parsing_networks:
                    if re.match(r"^[A-Za-z0-9\-\_]+:$", line):  # Network name (SSID)
                        if ssid:  # Save previous SSID before moving to the next
                            writer.writerow([timestamp, location, ssid, channel, security, rssi, band, status])
                            print(f"Saved: {timestamp}, {location}, {ssid}, {channel}, {security}, {rssi}, {band}, {status}")

                        ssid = line[:-1]  # Remove trailing ':' from SSID
                        channel, security, rssi, band = "", "", "", ""

                    elif "Channel:" in line:
                        channel = line.split(":")[1].strip().split(" ")[0]  # Extract only channel number
                        band = "2.4GHz" if int(channel) <= 14 else "5GHz"  # Determine band

                    elif "Security:" in line:
                        security = line.split(":")[1].strip()

                    elif "Signal / Noise:" in line:
                        rssi = line.split(":")[1].split("/")[0].strip()  # Extract signal value

            # Write the last detected network
            if ssid and channel and security and rssi:
                writer.writerow([timestamp, location, ssid, channel, security, rssi, band])
                print(f"Saved: {timestamp}, {location}, {ssid}, {channel}, {security}, {rssi}, {band}")

            counter += 1
            print(f"Data saved for {location}. Point {counter}")

    except KeyboardInterrupt:
        print("\nData collection stopped.")
