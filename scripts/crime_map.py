import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# File paths
geojson_path = "../data/world_boundaries.geojson"
csv_path = "../clean_data/crime_clean.csv"
output_geojson_path = "../plots/world_crime.geojson"

# Read GeoJSON and CSV into GeoDataFrame and DataFrame
gdf = gpd.read_file(geojson_path)
df = pd.read_csv(csv_path)

# Rename the "name" column to "Country" in the GeoDataFrame
gdf = gdf.rename(columns={'name': 'Country'})

# Merge GeoDataFrame with DataFrame based on the common column "Country"
merged_gdf = pd.merge(gdf, df[['Country', 'Resilience']], on='Country', how='left')

# Rename the new column as needed
merged_gdf = merged_gdf.rename(columns={'Resilience': 'Resilience'})

# Plot the GeoDataFrame
fig, ax = plt.subplots(figsize=(12, 12))
merged_gdf.plot(ax=ax, column='Resilience', cmap='coolwarm_r', linewidth=0.8, edgecolor='0.8',
                legend=True, legend_kwds={'label': "Resilience", 'orientation': "horizontal", 'shrink': 0.5})
ax.set_title('GeoJSON Plot with New Column', fontsize=16)
ax.set_axis_off()
plt.tight_layout()
plt.show()

# Save the merged GeoDataFrame back to GeoJSON
merged_gdf.to_file(output_geojson_path, driver='GeoJSON')

print(f"'name' column renamed, new column added, GeoJSON saved, and plot displayed.")