import geopandas as gpd
import rasterio

# Load the GeoJSON file
centroids = gpd.read_file('../data/output/centroids_classified_disaster_crime_merged.geojson')

# Open the raster file
with rasterio.open('../data/clean/climate_reclass.tif') as src:
    # Initialize a list to store the climate values
    climate_values = []

    # Iterate over each row in the GeoDataFrame
    for _, centroid in centroids.iterrows():
        # Get the raster value at the centroid's coordinates
        for val in src.sample([(centroid.geometry.x, centroid.geometry.y)]):
            climate_values.append(val[0])

# Add the climate values to the GeoDataFrame
centroids['climate'] = climate_values

# Save the GeoDataFrame to a new GeoJSON file
centroids.to_file('../data/output/centroids_final.geojson', driver='GeoJSON')