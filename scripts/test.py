import pandas as pd

# Load the data
data = pd.read_csv("../data/clean/crime_clean.csv")

# Print a statistical overview
print(data.describe())