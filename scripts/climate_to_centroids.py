import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np

# Load the GeoJSON file
centroids = gpd.read_file("../data/output/centroids_classified_disaster_crime_merged.geojson")

# Load the baden_wuerttemberg.geojson file
baden_wuerttemberg = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Open the raster file
with rasterio.open("../data/clean/climate_reclass.tif") as src:
    # Check the CRS of both files
    print(f"CRS of GeoJSON file: {centroids.crs}")
    print(f"CRS of raster file: {src.crs}")

    # If the CRS are different, convert the GeoJSON file to the CRS of the raster file
    if str(centroids.crs) != str(src.crs):
        centroids = centroids.to_crs(src.crs)

    # Clip the raster to the extent of the baden_wuerttemberg.geojson file
    out_image, out_transform = mask(src, [baden_wuerttemberg.geometry.unary_union], crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    # Write the clipped raster to a new file
    with rasterio.open("../data/clean/climate_reclass_clipped.tif", "w", **out_meta) as dest:
        dest.write(out_image)

# Open the clipped raster file
with rasterio.open("../data/clean/climate_reclass_clipped.tif") as src:
    # Initialize a list to store the climate values
    climate_values = []

    # Iterate over each row in the GeoDataFrame
    for _, centroid in centroids.iterrows():
        # Convert the centroid's coordinates to the raster's coordinate system
        x, y = src.index(centroid.geometry.x, centroid.geometry.y)

        # Check if the indices are within the bounds of the raster's array of pixel values
        if 0 <= x < src.width and 0 <= y < src.height:
            # Read the raster value at the centroid's coordinates
            raster_val = src.read(1)[y, x]
        else:
            # If the indices are out of bounds, set the raster value to a default value (e.g., np.nan)
            raster_val = np.nan

        # Append the raster value to the climate values list
        climate_values.append(raster_val)

# Add the climate values to the GeoDataFrame
centroids['climate'] = climate_values

# Save the GeoDataFrame to a new GeoJSON file
centroids.to_file("../data/output/centroids_final.geojson", driver='GeoJSON')