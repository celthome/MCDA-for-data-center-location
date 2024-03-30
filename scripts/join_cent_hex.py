import geopandas as gpd

# Load the GeoJSON files into GeoDataFrames
centroids = gpd.read_file("../data/output/centroids_final.geojson")
grid = gpd.read_file("../data/output/grid.geojson")

# Check the CRS of both files
print(f"CRS of centroids: {centroids.crs}")
print(f"CRS of grid: {grid.crs}")

# If the CRS are different, convert the GeoDataFrames to the right CRS
if centroids.crs != "EPSG:25832":
    centroids = centroids.to_crs("EPSG:25832")
if grid.crs != "EPSG:25832":
    grid = grid.to_crs("EPSG:25832")

# Perform a spatial join
joined = gpd.sjoin(grid, centroids, how='inner', op='intersects')

# If the joined GeoDataFrame is not empty, save it to a new GeoJSON file
if not joined.empty:
    # Drop unnecessary columns
    joined = joined.drop(columns=['cell_id', 'longitude', 'latitude'])

    # Save the resulting GeoDataFrame to a new GeoJSON file
    joined.to_file("../data/output/grid_prefinal.geojson", driver='GeoJSON')
else:
    print("The joined GeoDataFrame is empty.")