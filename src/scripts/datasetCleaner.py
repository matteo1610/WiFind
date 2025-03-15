import pandas as pd
import os
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Clean all CSV files in a given folder and save them in a subfolder.")
parser.add_argument('folder_path', help="Path to the folder containing CSV files")
args = parser.parse_args()

# Ensure the folder exists
if not os.path.isdir(args.folder_path):
    print(f"Error: Folder '{args.folder_path}' does not exist.")
    exit(1)

# Create the 'AW' subfolder if it doesn't exist
aw_folder = os.path.join(args.folder_path, 'AW')
os.makedirs(aw_folder, exist_ok=True)

# Process each CSV file in the folder
for file_name in os.listdir(args.folder_path):
    if file_name.endswith(".csv"):  # Process only CSV files
        input_file = os.path.join(args.folder_path, file_name)
        df = pd.read_csv(input_file)

        # Filter rows where SSID is 'ALMAWIFI'
        df_filtered = df[df['SSID'] == 'ALMAWIFI']

        # Keep only the relevant columns: Aula, Situazione, BSSID, SSID, Signal
        #df_filtered = df_filtered[['Aula', 'Situazione', 'BSSID', 'SSID', 'Signal']]

        # Create the output filename with 'AW' prefix and save it in the 'AW' subfolder
        new_filename = os.path.join(aw_folder, 'AW_' + file_name)

        # Save the cleaned data to a new CSV file
        df_filtered.to_csv(new_filename, index=False)

        print(f"Data has been cleaned and saved to '{new_filename}'.")
