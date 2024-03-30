import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Load the GeoJSON file into a GeoDataFrame
grid = gpd.read_file("../data/output/grid_prefinal.geojson")

# Define the weights for each column
weights = {
    # weights will be based on literature and climate friendliness
    # energy availability: powerline distance, powerplant distance, powerplant type
    # overall weight 0.35
    "classification_plant_source": 0.3,
    "classification_powerplant_distance": 0.04,
    "classification_powerline_distance": 0.01,
    #telecom availability: telecom line distance
    #overall weight 0.05
    "classification_telecom_distance": 0.05,
    #water availability: water quantity
    #overall weight 0.1
    "classification_water_area": 0.1,
    #protection: nature protection (national park etc.), protection class
    #overall weight 0.3
    "reclass_protect_class": 0.3,
    #index based on deaths due to natural hazards
    "hazards_reclassified": 0, #same values for Ba-Wü
    #reachability of each cell by different transport modes for potential workers, maintenance
    #overall weight 0.20
    #bike 0.08
    "bike_10min": 0.04,
    "bike_20min": 0.02,
    "bike_30min": 0.01,
    "bike_45min": 0.007,
    "bike_60min": 0.003,
    "car_10min": 0, # Set to 0 as data is missing and we want climate to have a higher impact anyway
    "car_20min": 0,
    "car_30min": 0,
    "car_45min": 0,
    "car_60min": 0,
    #walk 0.12
    "walk_10min": 0.05,
    "walk_20min": 0.035,
    "walk_30min": 0.02,
    "walk_45min": 0.01,
    "walk_60min": 0.005,
    #climate: climate index
    "climate": 0, #identical values for whole of Ba-Wü, also some missing values
}

# Replace NoData values with 0
grid = grid.fillna(0)

# Create the "fitness" column
grid["fitness"] = grid.apply(lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row), axis=1)

# Normalize the "fitness" values to a range between 0 and 10
grid["fitness"] = np.interp(grid["fitness"], (grid["fitness"].min(), grid["fitness"].max()), (0, 10))

# Round the "fitness" values to the nearest full number
grid["fitness"] = grid["fitness"].round().astype(int)

# Save the resulting GeoDataFrame to a new GeoJSON file
grid.to_file("../data/output/grid_final.geojson", driver='GeoJSON')


# Load the GeoJSON file into a GeoDataFrame
grid = gpd.read_file("../data/output/grid_final.geojson")

# Create a plot with the "fitness" column and the hexagon geometry
fig, ax = plt.subplots(1, 1)
grid.plot(column="fitness", cmap="viridis", linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Save the plot to a PNG file
plt.savefig("../plots/fitness_plot.png")

# Show the plot
plt.show()