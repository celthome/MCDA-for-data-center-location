"""
Author: Dominik Neumann, Celina Thomé
this script cleans the death-rate-from-natural-disasters-gbd.csv file to only contain the 30-year
average of disaster related deaths of all countries and selected regions
"""

import os

import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the CSV file
relative_path = "../data/death-rate-from-natural-disasters-gbd.csv"

# Create the absolute file path
file_path = os.path.join(script_dir, relative_path)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Rename the 4th column to "Deaths" using its index (3)
df = df.rename(columns={df.columns[3]: "Deaths"})

# Group the data by "Entity" aka country and calculate the average rate of deaths for each country
average_rates = df.groupby("Entity")["Deaths"].mean().reset_index()

# Print the result
print(average_rates)

# Replace 'output_file.csv' with the desired output file path
output_file_path = "../clean_data/clean_natural_hazards.csv"

# Write the result to a new CSV file
average_rates.to_csv(output_file_path, index=False)