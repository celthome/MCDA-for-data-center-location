import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, box, GeometryCollection
from ohsome import OhsomeClient
import matplotlib.pyplot as plt
from IPython.display import display
import geohexgrid as ghg

#top script should work step by step, bottom script is not tested yet but should be better. Data is provided regardless.

"""
Download power lines data from the ohsome API and saves it to a GeoJSON file.

client = OhsomeClient()

# Load the geojson file with geopandas
bpolys = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Define which OSM features should be considered for power lines.
filter_power_lines = "power=line"

# Specify the geometry type you want to retrieve (LineString for power lines)
geometry_type_power_lines = "LineString"

# Make the request to ohsome API for power lines
response_power_lines = client.elements.geometry.post(
    bpolys=bpolys,
    filter=filter_power_lines,
    properties="tags,metadata"
)

# Convert the response to a GeoDataFrame for power lines
power_lines_df = response_power_lines.as_dataframe()

# Display and plot the power lines GeoDataFrame
display(power_lines_df)
ax = power_lines_df.plot()

# Save the plot to a file using fig.savefig()
fig = ax.get_figure()
fig.savefig("../plots/powerlines.png", dpi=300, bbox_inches="tight")

# Save the power lines GeoDataFrame to a GeoJSON file
power_lines_df.to_file("../data/output/powerlines.geojson", driver='GeoJSON')


"""
#Download power plants data from the ohsome API and save it to a GeoJSON file.
"""

client = OhsomeClient()

# Load the geojson file with geopandas
bpolys = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Define which OSM features should be considered for power plants.
filter_power_plant = "power=plant"

# Make the request to ohsome API for power plants
response_power_plant = client.elements.geometry.post(
    bpolys=bpolys,
    filter=filter_power_plant,
    properties="tags,metadata"
)

# Convert the response to a GeoDataFrame for power plants
power_plant_df = response_power_plant.as_dataframe()

# Reproject to EPSG 25832 (ETRS89 / UTM Zone 32N)
bpolys = bpolys.to_crs(epsg=25832)
power_plant_df = power_plant_df.to_crs(epsg=25832)

# Some Features (very less) are points but most of them are polygons.
# So we buffer the points to faciliate further calculations.
# Define a function to create squares around each point or within a GeometryCollection
def create_square_around_geometry(geometry, side_length):
    if isinstance(geometry, Point):
        x, y = geometry.x, geometry.y
        half_side = side_length / 2
        return box(x - half_side, y - half_side, x + half_side, y + half_side)
    elif isinstance(geometry, GeometryCollection):
        return GeometryCollection([create_square_around_geometry(sub_geometry, side_length) for sub_geometry in geometry.geoms])
    else:
        return geometry  # For other geometry types, return as is

# Set the side length for the squares (adjust as needed)
square_side_length = 5

# Create squares around each point in the GeoDataFrame
power_plant_df['geometry'] = power_plant_df['geometry'].apply(
    lambda geometry: create_square_around_geometry(geometry, square_side_length)
)

# Display and plot the power plants GeoDataFrame with square polygons
display(power_plant_df)
ax = power_plant_df.plot()

# Reproject to EPSG 4326
bpolys = bpolys.to_crs(epsg=4326)
power_plant_df = power_plant_df.to_crs(epsg=4326)

# Save the plot to a file using fig.savefig()
fig = ax.get_figure()
fig.savefig("../plots/power_plants.png", dpi=300, bbox_inches="tight")

# Save the power plants GeoDataFrame with square polygons to a GeoJSON file
power_plant_df.to_file("../data/output/powerplants.geojson", driver='GeoJSON')


"""
#Download telecom points data from the ohsome API and save it to a GeoJSON file.
"""

client = OhsomeClient()

# Load the geojson file with geopandas
bpolys = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Define which OSM features should be considered for telecom
filter_telecom = "telecom=*"

# Make the request to ohsome API for telecom
response_telecom = client.elements.geometry.post(
    bpolys=bpolys,
    filter=filter_telecom,
    properties="tags,metadata"
)

# Convert the response to a GeoDataFrame for telecom
telecom_df = response_telecom.as_dataframe()

# Reproject to EPSG 25832 (ETRS89 / UTM Zone 32N)
bpolys = bpolys.to_crs(epsg=25832)
telecom_df = telecom_df.to_crs(epsg=25832)

# If you have Polygon geometries and you want to get the centroids, use the following:
telecom_df['geometry'] = telecom_df['geometry'].centroid

# Filter to include only Point geometries
telecom_points_df = telecom_df[telecom_df['geometry'].geom_type == 'Point']

# Display and plot the telecom points GeoDataFrame
display(telecom_points_df)
ax = telecom_points_df.plot()

# Reproject to EPSG 4326
bpolys = bpolys.to_crs(epsg=4326)
telecom_points_df = telecom_points_df.to_crs(epsg=4326)

# Save the plot to a file using fig.savefig()
fig = ax.get_figure()
fig.savefig("../plots/telecom_points.png", dpi=300, bbox_inches="tight")

# Save the telecom points GeoDataFrame to a GeoJSON file
telecom_points_df.to_file("../data/output/telecom_points.geojson", driver='GeoJSON')


"""
#Download water data from the ohsome API and save it to a GeoJSON file.
"""

client = OhsomeClient()

# Load the geojson file with geopandas
bpolys = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Define which OSM features should be considered for water
filter_water = "water=*"

# Make the request to ohsome API for water
response_water = client.elements.geometry.post(
    bpolys=bpolys,
    filter=filter_water,
    properties="tags,metadata"
)

# Convert the response to a GeoDataFrame for water
water_df = response_water.as_dataframe()

# Display and plot water GeoDataFrame
display(water_df)
ax = water_df.plot()

# Save the plot to a file using fig.savefig()
fig = ax.get_figure()
fig.savefig("../plots/water.png", dpi=300, bbox_inches="tight")

# Save the water GeoDataFrame to a GeoJSON file
water_df.to_file("../data/output/water.geojson", driver='GeoJSON')


"""
#Download nature reserve data from the ohsome API and save it to a GeoJSON file.
"""

client = OhsomeClient()

# Load the geojson file with geopandas
bpolys = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Define which OSM features should be considered for nature reserves.
filter_nature_reserve = "leisure=nature_reserve"

# Make the request to ohsome API for nature reserve
response_nature_reserve = client.elements.geometry.post(
    bpolys=bpolys,
    filter=filter_nature_reserve,
    properties="tags,metadata"
)

# Filter the response to include only polygons
nature_reserve_df = response_nature_reserve.as_dataframe()
nature_reserve_df = nature_reserve_df[nature_reserve_df.geometry.type == 'Polygon']

# Display and plot the nature reserves GeoDataFrame
display(nature_reserve_df)
nature_reserve_df.plot()

# Save the nature reserves GeoDataFrame to a GeoJSON file
nature_reserve_df.to_file("../data/output/nature_reserve.geojson", driver='GeoJSON')


"""
#Download protected area data from the ohsome API and save it to a GeoJSON file.
"""

client = OhsomeClient()

# Load the GeoJSON file with geopandas
bpolys = gpd.read_file("../data/input/baden_wuerttemberg.geojson")

# Define which OSM features should be considered for protected areas
filter_protected_area = "boundary=protected_area"

# Make the request to ohsome API for nature reserve
response_protected_area = client.elements.geometry.post(
    bpolys=bpolys,
    filter=filter_protected_area,
    properties="tags,metadata"
)

# Convert the response to a GeoDataFrame for protected areas
protected_area_df = response_protected_area.as_dataframe()

# Filter the GeoDataFrame to include only polygons and multi-polygons
filtered_protected_area_df = protected_area_df[protected_area_df.geom_type.isin(['Polygon', 'MultiPolygon'])]

# Display the filtered protected area GeoDataFrame
display(filtered_protected_area_df)

# Plot the protected area GeoDataFrame
filtered_protected_area_df.plot()

# Save the filtered protected areas GeoDataFrame to a GeoJSON file
filtered_protected_area_df.to_file("../data/output/protected_area.geojson", driver='GeoJSON')
"""



"""
shorter but not tested yet
"""

import geopandas as gpd
from ohsome import OhsomeClient
from IPython.display import display


def load_geojson(file_path):
    return gpd.read_file(file_path)

def reproject_gdf(gdf, epsg_code):
    return gdf.to_crs(epsg=epsg_code)

def save_gdf_to_geojson(gdf, file_path):
    gdf.to_file(file_path, driver='GeoJSON')

def display_and_plot_gdf(gdf, plot_file_path):
    display(gdf)
    ax = gdf.plot()
    fig = ax.get_figure()
    fig.savefig(plot_file_path, dpi=300, bbox_inches="tight")

def download_data_from_ohsome(filter, output_file_path):
    client = OhsomeClient()
    bpolys = load_geojson("../data/input/baden_wuerttemberg.geojson")
    response = client.elements.geometry.post(
        bpolys=bpolys,
        filter=filter,
        properties="tags,metadata"
    )
    gdf = response.as_dataframe()
    save_gdf_to_geojson(gdf, output_file_path)
    return gdf  # return the dataframe for further processing

# Download power lines data
power_lines_df = download_data_from_ohsome("power=line", "../data/input/powerlines.geojson")
display_and_plot_gdf(power_lines_df, "../plots/powerlines.png")

# Download power plants data
power_plant_df = download_data_from_ohsome("power=plant", "../data/input/powerplants.geojson")
display_and_plot_gdf(power_plant_df, "../plots/power_plants.png")

# Download telecom points data
telecom_points_df = download_data_from_ohsome("telecom=*", "../data/input/telecom_points.geojson")
display_and_plot_gdf(telecom_points_df, "../plots/telecom_points.png")

# Download water data
water_df = download_data_from_ohsome("water=*", "../data/input/water.geojson")
display_and_plot_gdf(water_df, "../plots/water.png")

# Download nature reserve data
nature_reserve_df = download_data_from_ohsome("leisure=nature_reserve", "../data/input/nature_reserve.geojson")
display_and_plot_gdf(nature_reserve_df, "../plots/nature_reserve.png")

# Download protected area data
protected_area_df = download_data_from_ohsome("boundary=protected_area", "../data/input/protected_area.geojson")
display_and_plot_gdf(protected_area_df, "../plots/protected_area.png")