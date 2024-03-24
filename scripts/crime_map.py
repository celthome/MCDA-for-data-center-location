import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# File paths
geojson_path = "../data/world_boundaries.geojson"
csv_path = "../clean_data/crime_clean.csv"
output_geojson_path = "../plots/world_crime.geojson"
output_plot_path = "../plots/world_crime_plot.png"

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
plot = merged_gdf.plot(ax=ax, column='Resilience', cmap='RdPu', linewidth=0.8, edgecolor='0.8')

# Create colorbar
norm = Normalize(vmin=merged_gdf['Resilience'].min(), vmax=merged_gdf['Resilience'].max())
sm = ScalarMappable(cmap='RdPu', norm=norm)
sm.set_array([])  # Fake array for ScalarMappable with colorbar

# Add colorbar to the plot
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.05, pad=0.05, shrink=0.3)
cbar.set_label('Resilience Index')

ax.set_title('Organized Crime Resilience', fontsize=16)
ax.set_axis_off()
plt.tight_layout()

# Save the plot
plt.savefig(output_plot_path, format='png', bbox_inches='tight', dpi=300)
plt.show()

# Save the merged GeoDataFrame back to GeoJSON
merged_gdf.to_file(output_geojson_path, driver='GeoJSON')

print("'name' column renamed, new column added, GeoJSON saved, colorbar plot saved, and plot displayed.")