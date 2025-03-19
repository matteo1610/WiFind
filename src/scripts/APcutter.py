# APCUTTER
# python3 APcutter.py path_to_csv.csv
# Out: mostra istogramma AP/numero di rilevazioni per AP
# Out: pulisce il .csv eliminando le colonne di APx 
    # che hanno un numero di valori rilevati sotto una soglia passata in input alla richiesta del programma

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot histogram of AP value counts from a CSV file.")
parser.add_argument("file", type=str, help="Path to the CSV file")
args = parser.parse_args()

# Load the CSV file
df = pd.read_csv(args.file)  # Use file from command-line argument

# Drop non-AP columns (assuming first two columns are not APs)
ap_columns = df.columns[2:]

# Count non-null values per AP
value_counts = df[ap_columns].count()

# Plot the histogram
plt.figure(figsize=(12, 6))
sns.barplot(x=value_counts.index, y=value_counts.values, color='skyblue')
plt.xticks(rotation=90)
#plt.ylim(0, 100)  # Set y-axis limit to 100
plt.xlabel("Access Points (APs)")
plt.ylabel("Number of Recorded Values")
plt.title(f"Number of Recorded Values per AP (Total APs: {len(ap_columns)})")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

y_threshold = input("Enter a threshold value to delete APs (or press Enter to skip): ")
if y_threshold.isdigit():
    y_threshold = int(y_threshold)
    
    # Filter AP columns based on threshold
    filtered_columns = [col for col in ap_columns if value_counts[col] >= y_threshold]
    remaining_ap_count = len(filtered_columns)
    
    # Create a new DataFrame with filtered columns
    df_filtered = df[['Aula', 'Situazione'] + filtered_columns]
    
    # Save new CSV file with _cut_y_apXX suffix
    new_filename = args.file.replace(".csv", f"_cut_{y_threshold}_ap{remaining_ap_count}.csv")
    df_filtered.to_csv(new_filename, index=False)
    print(f"Filtered CSV saved as {new_filename}")