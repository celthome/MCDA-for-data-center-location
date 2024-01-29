import pandas as pd

# File path of the input CSV file
input_csv_path = "../data/organized_crime_index.csv"

# File path for the output CSV file
output_csv_path = "../clean_data/crime_clean.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(input_csv_path, sep=";")

# Keep only the "Country" and "Resilience avg" columns
df = df[["Country", "Resilience avg,"]]

# Rename the "Resilience avg" column to "Resilience"
df = df.rename(columns={"Resilience avg,": "Resilience"})

# Save the modified DataFrame to a new CSV file
df.to_csv(output_csv_path, index=False, sep=",")

print(f"Columns filtered and renamed. Output saved to: {output_csv_path}")
