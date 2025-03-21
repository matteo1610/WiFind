import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_rssi(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file)
    
    # Identify columns to normalize (excluding "Aula" and "Situazione" if present)
    columns_to_normalize = df.columns[2:]  # Assuming the first two columns are categorical
    
    # Apply Min-Max Scaling
    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    
    # Replace NaN values with 0
    df_normalized.fillna(0, inplace=True)
    
    # Save the normalized dataset
    df_normalized.to_csv(output_file, index=False)
    
    print(f"Normalized dataset saved to: {output_file}")


if __name__ == "__main__":
    input_file = "../../data/processed/wifi_fingerprinting_dataset_cut_400_ap22.csv"
    output_file = "../../data/processed/wifi_fingerprinting_dataset_normalized.csv"
    normalize_rssi(input_file, output_file)
