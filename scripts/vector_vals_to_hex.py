import geopandas as gpd

def assign_vector_values_to_hexagons(hexagon_file, vector_file, attribute, output_column):
    """
    Assign vector values to hexagons based on their spatial overlap.

    Args:
    hexagon_file (str): Path to the GeoJSON file containing hexagons.
    vector_file (str): Path to the vector file containing factor values.
    attribute (str): The attribute in the vector data to calculate the mean of.
    output_column (str): Name of the column in the hexagon GeoDataFrame to write the results to.
    """
    # Load the hexagon and vector GeoJSON files
    hexagons = gpd.read_file(hexagon_file)
    vector = gpd.read_file(vector_file)

    # Perform a spatial join between the hexagons and the vector data
    joined = gpd.sjoin(hexagons, vector, how="inner", op="intersects")

    # Group by the hexagon ID and calculate the mean of the attribute
    results = joined.groupby(hexagons.index)[attribute].mean()

    # Assign the results to the specified column in the hexagon GeoDataFrame
    hexagons.loc[results.index, output_column] = results.values

    # Save the GeoDataFrame to a new GeoJSON file
    hexagons.to_file(hexagon_file, driver='GeoJSON')