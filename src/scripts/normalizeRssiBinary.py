import pandas as pd

def binarize_rssi(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # Identify columns to binarize (excluding "Aula" and "Situazione" if present)
    columns_to_binarize = df.columns[2:]  # Assuming the first two columns are categorical
    
    # Apply binarization (1 if value is present, 0 if NaN)
    df_binarized = df.copy()
    df_binarized[columns_to_binarize] = df[columns_to_binarize].notna().astype(int)
    
    # Save the binarized dataset
    df_binarized.to_csv(output_file, index=False)
    
    print(f"Binarized dataset saved to: {output_file}")

if __name__ == "__main__":
    input_file = "../../data/processed/wifi_fingerprinting_dataset_cut_400_ap22.csv"
    output_file = "../../data/processed/wifi_fingerprinting_dataset_binarized.csv"
    binarize_rssi(input_file, output_file)
