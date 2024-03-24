import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# File paths
geojson_path = "../data/world_boundaries.geojson"
csv_path = "../clean_data/clean_natural_hazards.csv"
output_geojson_path = "../plots/hazard_deaths.geojson"
output_plot_path = "../plots/hazard_plot.png"

# Read GeoJSON and CSV into GeoDataFrame and DataFrame
gdf = gpd.read_file(geojson_path)

# Read the new CSV file with "Entity" and "Deaths" columns
new_df = pd.read_csv(csv_path)

# Rename the "name" column to "Country" in the GeoDataFrame
gdf = gdf.rename(columns={'name': 'Country'})

# Rename the "Entity" column to "Country" in the new DataFrame
new_df = new_df.rename(columns={'Entity': 'Country'})

# Merge GeoDataFrame with new DataFrame based on the common column "Country"
merged_gdf = pd.merge(gdf, new_df[['Country', 'Deaths']], on='Country', how='left')

# Classify values into specified ranges
merged_gdf['Classified_Deaths'] = pd.cut(merged_gdf['Deaths'], bins=[-1, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99],
                                         labels=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1], include_lowest=True)

# Set the categories for 'Classified_Deaths' column
categories = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
merged_gdf['Classified_Deaths'] = pd.Categorical(merged_gdf['Classified_Deaths'], categories=categories, ordered=True)

# Replace NaN values with a specific value (e.g., 0) before converting to integers
merged_gdf['Classified_Deaths'] = merged_gdf['Classified_Deaths'].cat.add_categories(0).fillna(0).astype(int)

# Increase resolution and DPI
fig, ax = plt.subplots(figsize=(18, 18), dpi=300)

# Plot the GeoDataFrame with classified values (excluding 0)
plot = merged_gdf[merged_gdf['Classified_Deaths'] != 0].plot(ax=ax, column='Classified_Deaths', cmap='plasma', linewidth=0.8, edgecolor='0.8', legend=False)

# Create colorbar
norm = Normalize(vmin=1, vmax=10)
sm = ScalarMappable(cmap='plasma', norm=norm)
sm.set_array([])  # Fake array for ScalarMappable with colorbar

# Add colorbar to the plot
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.05, pad=0.05, shrink=0.3)
cbar.set_label('Classified Deaths')

ax.set_title('Natural Hazard Classified Deaths', fontsize=16)
ax.set_axis_off()
plt.tight_layout()

# Save the plot with higher resolution and DPI
plt.savefig(output_plot_path, format='png', bbox_inches='tight', dpi=300)
plt.show()

# Save the merged GeoDataFrame back to GeoJSON
merged_gdf.to_file(output_geojson_path, driver='GeoJSON')

print("'name' column renamed, new column added, GeoJSON saved, classified colorbar plot saved, and plot displayed.")