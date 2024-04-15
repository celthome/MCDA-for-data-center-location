import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from shapely.ops import nearest_points

warnings.simplefilter(action='ignore', category=FutureWarning)

"""
cleaning
"""

def clean_power_plants():
    # Load power plants GeoJSON file
    power_plants = gpd.read_file("../data/output/powerplants.geojson")

    # Replace the colon (:) with an underscore (_) in the column name
    power_plants.columns = power_plants.columns.str.replace(':', '_')

    # Save the modified GeoDataFrame to a new GeoJSON file
    power_plants.to_file("../data/output/powerplants.geojson", driver='GeoJSON')

def clean_crime_data():
    # File path of the input CSV file
    input_csv_path = "../data/organized_crime_index.csv"

    # File path for the output CSV file
    output_csv_path = "../clean_data/crime_clean.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path, sep=";")

    # Keep only the "Country" and "Resilience avg" columns
    df = df[["Country", "Resilience avg,"]]

    # Rename the "Resilience avg" column to "Resilience"
    df = df.rename(columns={"Resilience avg,": "Resilience"})

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False, sep=",")

def clean_natural_hazards_data():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the relative path to the CSV file
    relative_path = "../data/death-rate-from-natural-disasters-gbd.csv"

    # Create the absolute file path
    file_path = os.path.join(script_dir, relative_path)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Rename the 4th column to "Deaths" using its index (3)
    df = df.rename(columns={df.columns[3]: "Deaths"})

    # Group the data by "Entity" aka country and calculate the average rate of deaths for each country
    average_rates = df.groupby("Entity")["Deaths"].mean().reset_index()

    # Replace 'output_file.csv' with the desired output file path
    output_file_path = "../clean_data/clean_natural_hazards.csv"

    # Write the result to a new CSV file
    average_rates.to_csv(output_file_path, index=False)

"""
water area calculation
"""

def calculate_water_area(input_file_path, output_file_path):
    # Load water GeoJSON file
    water_gdf = gpd.read_file(input_file_path)

    # Filter out geometries that are polygons and create a copy
    water_polygons = water_gdf[water_gdf['geometry'].geom_type == 'Polygon'].copy()

    # Replace the colon (:) with an underscore (_) in the column names
    water_polygons.columns = water_polygons.columns.str.replace(':', '_')

    # Reproject the geometries to EPSG:25832
    water_polygons = water_polygons.to_crs(epsg=25832)

    # Calculate the area for each polygon and store it in a new column
    water_polygons['area'] = water_polygons['geometry'].area

    # Save the GeoDataFrame with polygons and the calculated area to a new GeoJSON file
    water_polygons.to_file(output_file_path, driver='GeoJSON')

"""
clip nature reserves
"""
def clip_nature_reserve(hexagon_grid_path, nature_reserve_path, output_geojson_path, output_plot_path):
    # Suppress the FutureWarning
    # warnings.simplefilter(action='ignore', category=FutureWarning)

    # Load hexagon grid and nature reserve data
    hexagon_grid = gpd.read_file(hexagon_grid_path)
    nature_reserve = gpd.read_file(nature_reserve_path)

    # Reproject geometries to a UTM CRS
    nature_reserve = nature_reserve.to_crs("EPSG:25832")

    # Clip nature reserve polygons at the borders of hexagons
    clipped_nature_reserve = gpd.overlay(nature_reserve, hexagon_grid, how='intersection', keep_geom_type=False)

    # Save the result
    clipped_nature_reserve.to_file(output_geojson_path, driver='GeoJSON')

    # Read the clipped nature reserve GeoJSON file
    clipped_nature_reserve = gpd.read_file(output_geojson_path)

    # Plot the clipped nature reserve
    fig, ax = plt.subplots(figsize=(10, 10))
    clipped_nature_reserve.plot(ax=ax, color='green', edgecolor='green')
    ax.set_title('Clipped Nature Reserve')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    # Save the plot to a file using fig.savefig()
    fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")


"""
clip protected area
"""

def clip_protected_area(hexagon_grid_path, protected_area_path, output_geojson_path, output_plot_path):
    # Suppress the FutureWarning
    # warnings.simplefilter(action='ignore', category=FutureWarning)

    # Load hexagon grid and protected area data
    hexagon_grid = gpd.read_file(hexagon_grid_path)
    protected_area = gpd.read_file(protected_area_path)

    # Reproject geometries to a UTM CRS
    protected_area = protected_area.to_crs("EPSG:25832")

    # Clip protected area polygons at the borders of hexagons
    clipped_protected_area = gpd.overlay(protected_area, hexagon_grid, how='intersection', keep_geom_type=False)

    # Save the result
    clipped_protected_area.to_file(output_geojson_path, driver='GeoJSON')

    # Read the clipped protected area GeoJSON file
    clipped_protected_area = gpd.read_file(output_geojson_path)

    # Plot the clipped protected area
    fig, ax = plt.subplots(figsize=(10, 10))
    clipped_protected_area.plot(ax=ax, color='maroon', edgecolor='maroon')
    hexagon_grid.plot(ax=ax, facecolor='none', edgecolor='grey')
    ax.set_title('Clipped Protected Areas with Hexagon Grid')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    # Save the plot to a file using fig.savefig()
    fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")

"""
distance calculation
"""

def calculate_distance_to_poi(centroids_path, poi_paths, output_directory):
    # Load centroids data with GeoPandas
    centroids = gpd.read_file(centroids_path)

    # Reproject centroids to EPSG:25832
    centroids = centroids.to_crs(epsg=25832)

    for poi_path in poi_paths:
        # Load points of interest data with GeoPandas
        points_of_interest = gpd.read_file(poi_path)

        # Extract the name of the point of interest from the file path
        poi_name = os.path.basename(poi_path).split('.')[0]

        # Reproject points of interest to EPSG:25832
        points_of_interest = points_of_interest.to_crs(epsg=25832)

        # Buffer the points of interest to avoid invalid geometries
        points_of_interest['geometry'] = points_of_interest.geometry.buffer(0)

        # Calculate distance between each centroid and the nearest point of interest
        distances = []
        nearest_poi = []

        for idx, centroid in centroids.iterrows():
            nearest_point = nearest_points(centroid.geometry, points_of_interest.unary_union)[1]
            distance = centroid.geometry.distance(nearest_point)
            distances.append(distance)
            nearest_poi.append(points_of_interest.iloc[points_of_interest.distance(nearest_point).idxmin()]['type'])
            print(f"Shortest distance for centroid {idx} to {poi_name} calculated and saved.")

        # Add the distances and nearest point of interest information to the centroids dataframe
        centroids[f'distance_to_{poi_name}'] = distances
        centroids[f'nearest_{poi_name}'] = nearest_poi

        # Save the GeoDataFrame to GeoJSON
        centroids.to_file(os.path.join(output_directory, f'centroids_with_{poi_name}_distances.geojson'), driver='GeoJSON')


# Call the function

# Define the paths to the centroids and points of interest GeoJSON files
centroids_path = '../data/output/centroids.geojson'
poi_paths = ['../data/output/water_area.geojson'] #'../data/output/telecom_points.geojson', '../data/output/powerplants.geojson', '../data/output/powerlines.geojson'

# Add a 'type' column to each GeoDataFrame in poi_paths
for gdf_path in poi_paths:
    gdf = gpd.read_file(gdf_path)
    gdf['type'] = os.path.basename(gdf_path).split('.')[0]
    gdf.to_file(gdf_path, driver='GeoJSON')  # Save the GeoDataFrame back to the file

# Define the output directory
output_directory = '../data/output/'

# Call the function
calculate_distance_to_poi(centroids_path, poi_paths, output_directory)

"""
    # Call the clip_protected_area function
    clip_protected_area('../data/output/grid.geojson', '../data/output/protected_area.geojson',
                        '../data/output/clip_protected_area.geojson', '../data/output/clip_protected_area.png')

    # Call the clip_nature_reserve function
    clip_nature_reserve('../data/output/grid.geojson', '../data/output/nature_reserve.geojson',
                        '../data/output/clip_nature_reserve.geojson', '../data/output/clip_nature_reserve.png')

    # Save the GeoDataFrame to GeoJSON
    #centroids.to_file('../data/output/distance.geojson', driver='GeoJSON')
"""

