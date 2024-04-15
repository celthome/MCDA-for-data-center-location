import rasterio
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

class RasterData:
    """
    A class used to represent and manipulate raster data.

    Attributes
    ----------
    input_file : str
        The path to the input raster file.
    output_file : str
        The path to the output raster file.
    num_classes : int
        The number of classes for reclassification.
    class_ranges : list of tuples
        The ranges for each class.
    class_values : list of int
        The values for each class.
    """
    def __init__(self, input_file, output_file, num_classes, class_ranges, class_values):
        self.input_file = input_file
        self.output_file = output_file
        self.num_classes = num_classes
        self.class_ranges = class_ranges
        self.class_values = class_values

    def reclassify_raster_data(self):
        """
        Reclassifies the raster data based on the class ranges and values.

        Returns
        -------
        numpy.ndarray
            The reclassified raster data.
        """
        with rasterio.open(self.input_file) as src:
            raster_data = src.read(1)
            reclassified_data = np.zeros_like(raster_data)
            for i in range(self.num_classes):
                min_val, max_val = self.class_ranges[i]
                new_val = self.class_values[i]
                reclassified_data[(raster_data >= min_val) & (raster_data <= max_val)] = new_val
            meta = src.meta
        with rasterio.open(self.output_file, 'w', **meta) as dst:
            dst.write(reclassified_data, 1)
        return reclassified_data

    def plot_and_save_raster_data(self, data, output_plot_path):
        """
        Plots and saves the raster data.

        Parameters
        ----------
        data : numpy.ndarray
            The raster data to plot.
        output_plot_path : str
            The path to save the plot.
        """
        plt.figure(figsize=(10, 8))
        img = plt.imshow(data, cmap="Greens", interpolation="none")
        cbar = plt.colorbar(img, label="Value", shrink=0.5)
        plt.xticks([])
        plt.yticks([])
        plt.title("Class Fitness")
        plt.tight_layout()
        plt.savefig(output_plot_path, format='png', dpi=300)
        print(f"Plot saved to: {output_plot_path}")
        plt.show()


def reclassify_vector(gdf, attribute, num_classes, class_ranges, class_values, new_column_name):
    """
    Reclassifies the vector data based on the class ranges and values.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        The GeoDataFrame to be reclassified.
    attribute : str
        The attribute to be reclassified.
    num_classes : int
        The number of classes for reclassification.
    class_ranges : list of tuples
        The ranges for each class.
    class_values : list of int
        The values for each class.
    new_column_name : str
        The name of the new column to be added to the GeoDataFrame.

    Returns
    -------
    geopandas.GeoDataFrame
        The reclassified vector data.
    """
    # Initialize reclassified column with zeros
    gdf[new_column_name] = 0

    # Loop through each class and reclassify the vector
    for i in range(num_classes):
        min_val, max_val = class_ranges[i]
        new_val = class_values[i]
        # Convert the entire column to float type
        gdf[attribute] = gdf[attribute].astype(float)
        # Handle NaN values
        gdf[attribute] = gdf[attribute].fillna(0)

        gdf.loc[(gdf[attribute] >= min_val) & (gdf[attribute] <= max_val), new_column_name] = new_val

    return gdf

def plot_and_save_reclassified(data, output_plot_path):
    # Plot the reclassified data
    fig, ax = plt.subplots(1, 1)
    data.plot(column='reclassified', ax=ax, legend=True)

    # Save the plot
    plt.savefig(output_plot_path, format='png', dpi=300)
    print(f"Plot saved to: {output_plot_path}")

    # Show the plot
    plt.show()

"""
Reclassify the natural hazards data
manually choose the class ranges and values
"""

# Define your parameters
input_file = "../data/clean/clean_natural_hazards.csv"
output_file = "../data/output/grid_prefinal.geojson"
attribute = "Deaths"  # replace with the attribute you want to reclassify
num_classes = 5  # replace with the number of classes you want
class_ranges = [(0, 0), (0, 0.1), (0.1, 0.5), (0.5, 1), (1, float("inf"))]  # replace with your class ranges
class_values = [10, 8, 7, 6, 2]  # replace with your class values

# Load the initial GeoJSON file
gdf = gpd.read_file(input_file)

# Perform the reclassification operation
gdf = reclassify_vector(gdf, attribute, num_classes, class_ranges, class_values, "Deaths")

# Save the resulting GeoDataFrame to a new GeoJSON file
gdf.to_file(output_file, driver='GeoJSON')

print("Natural hazards reclassification complete")


"""
Reclassify the crime data
manually choose the class ranges and values
"""

# Define your parameters for the next operation
input_file = "../data/clean/crime_clean.csv"
attribute = "Resilience"
num_classes = 10
class_ranges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
class_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Load the GeoJSON file from the previous operation
gdf = gpd.read_file(output_file)

# Load the new input file
gdf_new = gpd.read_file(input_file)

# Merge the two GeoDataFrames
gdf = gdf.merge(gdf_new, how='left')

# Perform the next reclassification operation
gdf = reclassify_vector(gdf, attribute, num_classes, class_ranges, class_values, "Resilience")

# Save the resulting GeoDataFrame to the same GeoJSON file
gdf.to_file(output_file, driver='GeoJSON')

print("Crime reclassification complete")


class TransportData:
    """
    A class used to represent and manipulate transport data.

    Attributes
    ----------
    mode : str
        The mode of transport.
    total_pop : int
        The total population.
    """
    def __init__(self, mode, total_pop):
        """
         Constructs all the necessary attributes for the TransportData object.

         Parameters
         ----------
         mode : str
             The mode of transport.
         total_pop : int
             The total population.
         """
        self.mode = mode
        self.total_pop = total_pop

    def calculate_transport_index(self, time_seconds):
        """
        Calculates the transport index.

        Parameters
        ----------
        time_seconds : int
            The time in seconds.

        Returns
        -------
        float
            The calculated transport index.
        """
        index = (3600 - time_seconds) * (self.total_pop / 8128445)
        return index

    @staticmethod
    def assign_transport_class(index):
        """
        Assigns a transport class based on the index.

        Parameters
        ----------
        index : float
            The transport index.

        Returns
        -------
        int
            The assigned transport class.
        """
        if index >= 90:
            return 10
        elif index >= 80:
            return 9
        elif index >= 70:
            return 8
        elif index >= 60:
            return 7
        elif index >= 50:
            return 6
        elif index >= 40:
            return 5
        elif index >= 30:
            return 4
        elif index >= 20:
            return 3
        elif index >= 10:
            return 2
        else:
            return 1

    def process_transport_geojson(self, gdf, new_column_name):
        """
        Processes the transport GeoJSON file.

        Parameters
        ----------
        gdf : geopandas.GeoDataFrame
            The GeoDataFrame to be processed.
        new_column_name : str
            The name of the new column to be added to the GeoDataFrame.

        Returns
        -------
        geopandas.GeoDataFrame
            The processed GeoDataFrame.
        """
        gdf[new_column_name] = gdf['value'].apply(self.calculate_transport_index)
        gdf[new_column_name] = gdf[new_column_name].apply(self.assign_transport_class)
        return gdf

class DistanceData:
    """
    A class used to represent and manipulate distance data.

    Attributes
    ----------
    distance_type : str
        The type of distance.
    """
    def __init__(self, distance_type):
        """
        Constructs all the necessary attributes for the DistanceData object.

        Parameters
        ----------
        distance_type : str
            The type of distance.
        """
        self.distance_type = distance_type

    @staticmethod
    def classify_distance_data(distance):
        """
        Classifies the distance data.

        Parameters
        ----------
        distance : float
            The distance.

        Returns
        -------
        int
            The classified distance data.
        """
        class_ranges = [(0, 1000), (1000, 2000), (2000, 3000), (3000, 4000), (4000, 5000),
                        (5000, 6000), (6000, 7000), (7000, 8000), (8000, 9000), (9000, float('inf'))]
        for i, (start, end) in enumerate(class_ranges, start=1):
            if start <= distance < end:
                return i

    def process_distance_geojson(self, gdf, new_column_name):
        """
        Processes the distance GeoJSON file.

        Parameters
        ----------
        gdf : geopandas.GeoDataFrame
            The GeoDataFrame to be processed.
        new_column_name : str
            The name of the new column to be added to the GeoDataFrame.

        Returns
        -------
        geopandas.GeoDataFrame
            The processed GeoDataFrame.
        """
        gdf[new_column_name] = gdf[f'distance_to_{self.distance_type}'].apply(self.classify_distance_data)
        return gdf


def process_geojson(gdf, input_file, data_class, new_column_name):
    # Load the new input file
    gdf_new = gpd.read_file(input_file)

    # Merge the two GeoDataFrames
    gdf = gdf.merge(gdf_new, how='left')

    # Process the GeoJSON
    gdf = data_class.process_geojson(gdf, new_column_name)

    return gdf

# Load the GeoJSON file from the previous operation
gdf = gpd.read_file(output_file)

for mode in ['car', 'bike', 'walk']:
    # Define the total population for each mode
    total_pop = {
        'car': 8128445,
        'bike': 1269190,
        'walk': 236125
    }[mode]

    # Create a TransportData object
    transport_data = TransportData(mode, total_pop)

    # Process the transport GeoJSON
    gdf = process_geojson(gdf, f"../data/output/isochrones_{mode}/{mode}_10min.geojson", transport_data, f'classification_{mode}_index')

# Save the resulting GeoDataFrame to the same GeoJSON file
gdf.to_file(output_file, driver='GeoJSON')

print("Transport reclassification complete")

for distance_type in ['powerplant', 'powerline', 'telecom']:
    # Create a DistanceData object
    distance_data = DistanceData(distance_type)

    # Process the distance GeoJSON
    gdf = process_geojson(gdf, f"../data/output/classified_{distance_type}.geojson", distance_data, f'classification_{distance_type}_distance')

# Save the resulting GeoDataFrame to the same GeoJSON file
gdf.to_file(output_file, driver='GeoJSON')

print("Distance reclassification complete")

# Merge the two GeoDataFrames on the 'cell_id' column

# Load the grid_with_centroids GeoJSON
gdf_centroids = gpd.read_file('data/output/grid_with_centroids.geojson')

# Merge the two GeoDataFrames on the 'cell_id' column
gdf_merged = gdf_centroids.merge(gdf, left_on='cell_id', right_on='id')

# Save the merged GeoDataFrame to a new GeoJSON file
gdf_merged.to_file('data/output/grid_prefinal.geojson', driver='GeoJSON')