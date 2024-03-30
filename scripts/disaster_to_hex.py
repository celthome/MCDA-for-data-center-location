import geopandas as gpd

# Load the GeoJSON files
natural_hazards = gpd.read_file('../data/output/natural_hazards_reclass.geojson')
centroids_classified = gpd.read_file('../data/output/centroids_classified.geojson')

# Extract the value of the "Germany" row
germany_value = natural_hazards.loc[natural_hazards['Entity'] == 'Germany', 'reclassified'].values[0]

# Append the value to each row of the centroids_classified dataframe in a new column
centroids_classified['hazards_reclassified'] = germany_value

# Save the updated dataframe to a new GeoJSON file
centroids_classified.to_file('../data/output/centroids_classified_disaster.geojson', driver='GeoJSON')