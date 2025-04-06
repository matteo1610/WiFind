# FINALDATASET
# python3 finalDataset.py path_to_ALMAWIFI_filtered_files
# Crea un dataset csv unico raccogliendo e rielaborando i dati dei dataset filtrati ALMAWIFI
# Out: 1 file finale

import os
import sys
import pandas as pd

def process_csv_files(folder_path, output_file="wifi_fingerprinting_dataset.csv"):
    unique_bssids = set()
    all_data = []

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Read all CSV files and collect data
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            all_data.append(df)
            unique_bssids.update(df["BSSID"])

    # Merge all data into a single DataFrame
    full_df = pd.concat(all_data, ignore_index=True)

    # Get unique BSSIDs and assign progressive AP names
    unique_bssids = sorted(unique_bssids)
    bssid_to_ap = {bssid: f"AP{i+1}" for i, bssid in enumerate(unique_bssids)}

    # Create the pivot table structure without aggregation
    pivot_df = full_df.pivot(index=["Timestamp", "Aula", "Situazione"], 
                              columns="BSSID", 
                              values="Signal")

    # Reset index to flatten the table
    pivot_df.reset_index(inplace=True)

    # Rename columns using progressive AP names
    pivot_df.columns = [bssid_to_ap[col] if col in bssid_to_ap else col for col in pivot_df.columns]

    # Remove the Timestamp column
    pivot_df.drop(columns=['Timestamp'], inplace=True)

    # Define the custom order for 'Aula' and 'Situazione'
    aula_order = ['E1', 'E2', 'E3', 'Corridor', 'Garden']
    situation_order = ['Empty', 'Crowded']

    # Create a categorical type for sorting
    pivot_df['Aula'] = pd.Categorical(pivot_df['Aula'], categories=aula_order, ordered=True)
    pivot_df['Situazione'] = pd.Categorical(pivot_df['Situazione'], categories=situation_order, ordered=True)

    # Sort the DataFrame
    pivot_df.sort_values(by=['Situazione', 'Aula'], inplace=True)


    # Create the 'processed' folder at the same level as the script

    script_dir = os.path.dirname(os.path.abspath(__file__))
    processed_folder = os.path.join(script_dir, "processed")
    os.makedirs(processed_folder, exist_ok=True)

    # Save to CSV in the 'processed' folder
    output_path = os.path.join(processed_folder, output_file)
    pivot_df.to_csv(output_path, index=False)
    print(f"Processed data saved to '{output_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_csv_files(folder_path)