import geopandas as gpd
import rasterio
from scripts.raster_vals_to_hex import assign_raster_values_to_hexagons

# Define your parameters
hexagon_file = "../data/grid.geojson"
raster_file = "../clean_data/climate_reclass.tif"
output_column = "Climate"  # The column to write the results to

# Load the hexagon GeoJSON file
hexagons = gpd.read_file(hexagon_file)
print(hexagons.crs)

# Open the raster file
with rasterio.open(raster_file) as src:
    print(src.crs)

    # Convert the GeoDataFrame to the same CRS as the raster file
    hexagons = hexagons.to_crs(src.crs)

# Save the converted GeoDataFrame back to the hexagon_file
hexagons.to_file(hexagon_file, driver='GeoJSON')

# Call the function
assign_raster_values_to_hexagons(hexagon_file, raster_file, output_column)