import geopandas as gpd
import pandas as pd

# File paths
geojson_path = "../data/world_boundaries.geojson"
csv_path = "../clean_data/clean_natural_hazards.csv"

# Read GeoJSON and CSV into GeoDataFrame and DataFrame
gdf_original = gpd.read_file(geojson_path)
df_csv = pd.read_csv(csv_path)

# Extract values of the "name" column from GeoJSON
name_values_geojson = set(gdf_original['name'])

# Extract values of the "Country" column from CSV, sort alphabetically, and convert to list
country_values_csv = sorted(set(df_csv['Entity']))

# Find values that exist only in one of the columns
unique_values_geojson = name_values_geojson - set(country_values_csv)
unique_values_csv = set(country_values_csv) - name_values_geojson

# Print or use the unique values as needed
print("Values unique to 'name' column in GeoJSON:")
print(sorted(list(unique_values_geojson)))

print("\nValues unique to 'Country' column in CSV:")
print(sorted(list(unique_values_csv)))