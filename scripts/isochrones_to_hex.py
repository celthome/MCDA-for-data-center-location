import numpy as np
import pandas as pd
import os
import geopandas as gpd

# bike

# Get a list of all files in the directory
directory = '../data/output/isochrones_bike/'
files = os.listdir(directory)

# Initialize an empty DataFrame with the required columns
new_df = pd.DataFrame(columns=["id", "bike_10min", "bike_20min", "bike_30min", "bike_45min", "bike_60min"])

# Initialize a counter for the 'id' values
id_counter = 1

# Iterate over files that contain "reclass" in their name
for file in files:
    if "reclass" not in file:
        continue

    # Read the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(os.path.join(directory, file))

    # Check if 'class' column exists in the GeoDataFrame
    if 'class' in gdf.columns:
        # Extract the value of the "class" column for each feature
        values = gdf['class'].values.tolist()

        # Create a new row with the values and the current 'id' value
        new_row = {"id": id_counter}
        new_row.update({new_df.columns[j+1]: values[j] for j in range(len(new_df.columns)-1)})

        # Append the new row to the DataFrame
        new_df = new_df.append(new_row, ignore_index=True)

        # Increment the 'id' counter
        id_counter += 1

# Write the DataFrame to a new CSV file
new_df.to_csv("../data/output/iso_bike_test.csv", index=False)

"""
# car

# Get a list of all files in the directory
directory = '../data/output/isochrones_car/'
files = os.listdir(directory)

# Initialize an empty DataFrame with the required columns
new_df = pd.DataFrame(columns=["id", "car_10min", "car_20min", "car_30min", "car_45min", "car_60min"])

# Initialize a counter for the 'id' values
id_counter = 1

# Define the iteration steps where a row with 'nodata' values should be inserted
nodata_steps = [33, 83, 97, 118, 129, 158]

# Iterate over files that contain "reclass" in their name
for i, file in enumerate(files):
    if "reclass" not in file:
        continue

    # If the current iteration step is in nodata_steps, append a row with 'nodata' values and skip the rest of the loop
    if i+1 in nodata_steps:
        new_row = {"id": id_counter, "car_10min": np.nan, "car_20min": np.nan, "car_30min": np.nan, "car_45min": np.nan, "car_60min": np.nan}
        new_df = new_df.append(new_row, ignore_index=True)
        id_counter += 1
        continue

    # Read the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(os.path.join(directory, file))

    # Check if 'class' column exists in the GeoDataFrame
    if 'class' in gdf.columns:
        # Extract the value of the "class" column for each feature
        values = gdf['class'].values.tolist()

        # Create a new row with the values and the current 'id' value
        new_row = {"id": id_counter}
        new_row.update({new_df.columns[j+1]: values[j] for j in range(len(new_df.columns)-1)})

        # Append the new row to the DataFrame
        new_df = new_df.append(new_row, ignore_index=True)

    # Increment the 'id' counter
    id_counter += 1

# Write the DataFrame to a new CSV file
new_df.to_csv("../data/output/iso_car_test.csv", index=False)

"""
# walk

# Get a list of all files in the directory
directory = '../data/output/isochrones_walk/'
files = os.listdir(directory)

# Initialize an empty DataFrame with the required columns
new_df = pd.DataFrame(columns=["id", "walk_10min", "walk_20min", "walk_30min", "walk_45min", "walk_60min"])

# Initialize a counter for the 'id' values
id_counter = 1

# Iterate over files that contain "reclass" in their name
for file in files:
    if "reclass" not in file:
        continue

    # Read the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(os.path.join(directory, file))

    # Check if 'class' column exists in the GeoDataFrame
    if 'class' in gdf.columns:
        # Extract the value of the "class" column for each feature
        values = gdf['class'].values.tolist()

        # Create a new row with the values and the current 'id' value
        new_row = {"id": id_counter}
        new_row.update({new_df.columns[j+1]: values[j] for j in range(len(new_df.columns)-1)})

        # Append the new row to the DataFrame
        new_df = new_df.append(new_row, ignore_index=True)

        # Increment the 'id' counter
        id_counter += 1

# Write the DataFrame to a new CSV file
new_df.to_csv("../data/output/iso_walk_test.csv", index=False)

# merge csv files

# Read the CSV files into DataFrames
df_bike = pd.read_csv("../data/output/iso_bike_test.csv")
#df_car = pd.read_csv("../data/output/iso_car_test.csv")
df_walk = pd.read_csv("../data/output/iso_walk_test.csv")

# Merge the DataFrames on the 'id' column
df_merged = df_bike.merge(df_walk, on='id')

# Write the merged DataFrame to a new CSV file
df_merged.to_csv("../data/output/iso_merged.csv", index=False)



# merge csv with geojson

# Read the GeoJSON file into a GeoDataFrame
gdf_centroids = gpd.read_file("../data/output/centroids_classified_disaster_crime.geojson")

# Convert the 'id' column to int for proper merging
gdf_centroids['id'] = gdf_centroids['id'].astype(int)

# Merge the GeoDataFrame with df_merged on the 'id' column
gdf_merged = gdf_centroids.merge(df_merged, left_on='id', right_on='id')

# Write the merged GeoDataFrame to a new GeoJSON file
gdf_merged.to_file("../data/output/centroids_classified_disaster_crime_merged.geojson", driver='GeoJSON')