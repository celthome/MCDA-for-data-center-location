import geopandas as gpd
import matplotlib.pyplot as plt
import geohexgrid as ghg
import json
import os
import time
from openrouteservice import Client
from openrouteservice.exceptions import ApiError

def load_geojson_and_reproject(file_path, epsg_code):
    gdf = gpd.read_file(file_path)
    return gdf.to_crs(epsg=epsg_code)

def save_gdf_to_geojson(gdf, file_path):
    gdf.to_file(file_path, driver='GeoJSON')
"""
def plot_and_save_gdf(gdf, plot_file_path):
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color='red', markersize=50, alpha=0.7, label='Centroids')
    ax.set_title('Isochrones for Cars')
    ax.legend()
    fig.savefig(plot_file_path, dpi=300, bbox_inches="tight")
    plt.show()

def calculate_isochrones_with_retry(client, coordinate, profile, range_type, range_seconds):
    retries = 3  # Number of retries
    for attempt in range(retries):
        try:
            isochrones = client.isochrones(locations=[coordinate], profile=profile, range_type=range_type, range=range_seconds, attributes=['total_pop'])
            return isochrones
        except ApiError as e:
            if "rate limit exceeded" in str(e):
                print(f"Rate limit exceeded. Retrying in 10 seconds...")
                time.sleep(10)  # Retry after 10 seconds for rate limit errors
            elif "Unable to build an isochrone map" in str(e):
                print(f"Unable to build an isochrone map for centroid. Skipping...")
                return None
            else:
                raise e  # Re-raise the exception if it's not related to rate limit exceeded
    return None

def calculate_isochrones_for_centroids(client, centroids, profile, range_type, range_seconds, output_directory):
    for idx, row in centroids.iterrows():
        lon, lat = row['geometry'].x, row['geometry'].y
        coordinate = (lon, lat)
        isochrones = calculate_isochrones_with_retry(client, coordinate, profile, range_type, range_seconds)
        if isochrones is None:
            continue
        output_filename = os.path.join(output_directory, f'isochrones_{profile}_{row["id"]}.geojson')
        with open(output_filename, 'w') as output_file:
            json.dump(isochrones, output_file)
        print(f"Isochrones calculated for centroid {row['id']}")
        time.sleep(1)
"""
# Load Baden-Württemberg territorial authorities and reproject
bw = load_geojson_and_reproject("../data/input/baden_wuerttemberg.geojson", 25832)

# Cover it minimally with hexagons of circumradius 10 kilometres
grid = ghg.make_grid_from_gdf(bw, R=10_000)

"""
# Initialize OpenRouteService client
api_key = ""  # Replace with your actual API key
client = Client(key=api_key)

# Define parameters for isochrone calculation
profiles = ['driving-car', 'cycling-regular', 'foot-walking']  # Update this list as per your requirements
range_type = 'time'
range_seconds = [600, 1200, 1800, 2700, 3600]  # Define desired time ranges in seconds

# Iterate over profiles and calculate isochrones
for profile in profiles:
    output_directory = f'../data/output/isochrones_{profile}/'
    os.makedirs(output_directory, exist_ok=True)
    centroids = load_geojson_and_reproject('../data/output/centroids_with_coordinates.geojson', "4326")
    calculate_isochrones_for_centroids(client, centroids, profile, range_type, range_seconds, output_directory)
    print(f"Isochrone calculation for {profile} completed.")
    plot_and_save_gdf(centroids, f"../plots/isochrones_{profile}_map.png")
"""
import geopandas as gpd

# Calculate centroids of hexagons
centroids = grid.geometry.centroid

# Create a new GeoDataFrame from the centroids
centroids_gdf = gpd.GeoDataFrame(geometry=centroids)

# Assign an ID to each centroid
centroids_gdf['id'] = range(1, len(centroids_gdf) + 1)

# Add longitude and latitude columns
centroids_gdf['longitude'] = centroids_gdf.geometry.x
centroids_gdf['latitude'] = centroids_gdf.geometry.y

# Save the centroids GeoDataFrame to a GeoJSON file
centroids_gdf.to_file("../data/output/centroids.geojson", driver='GeoJSON')

# Load the GeoJSON files into GeoDataFrames
centroids_new = gpd.read_file("../data/output/centroids.geojson")
grid_new = gpd.read_file("../data/output/grid.geojson")

# Check the CRS of both files
print(f"CRS of centroids: {centroids_new.crs}")
print(f"CRS of grid: {grid_new.crs}")

# If the CRS are different, convert the GeoDataFrames to the right CRS
if centroids_new.crs != "EPSG:25832":
    centroids_new = centroids_new.to_crs("EPSG:25832")
if grid_new.crs != "EPSG:25832":
    grid_new = grid_new.to_crs("EPSG:25832")

# Perform a spatial join
joined = gpd.sjoin(grid_new, centroids_new, how='inner', op='intersects')

# If the joined GeoDataFrame is not empty, save it to a new GeoJSON file
if not joined.empty:
    # Save the resulting GeoDataFrame to a new GeoJSON file
    joined.to_file("../data/output/joined.geojson", driver='GeoJSON')
else:
    print("The joined GeoDataFrame is empty.")