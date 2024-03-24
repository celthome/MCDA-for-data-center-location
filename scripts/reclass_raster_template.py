import numpy as np
import rasterio
import matplotlib.pyplot as plt

def reclassify_raster(input_file, output_file, num_classes, class_ranges, class_values):
    """
    Reclassify a georeferenced raster file into a specified number of classes.

    Args:
    input_file (str): Path to the input raster file.
    output_file (str): Path to save the reclassified raster file.
    num_classes (int): Number of new classes.
    class_ranges (list): List of tuples specifying the range of values for each class.
                         Example: [(0, 100), (101, 200), (201, 300)]
    class_values (list): List of new values for each class, between 0 and 10.
                         Example: [0, 5, 10]
    """
    # Open the input raster file
    with rasterio.open(input_file) as src:
        # Read raster data as numpy array
        raster_data = src.read(1)

        # Initialize reclassified array with zeros
        reclassified_data = np.zeros_like(raster_data)

        # Loop through each class and reclassify the raster
        for i in range(num_classes):
            min_val, max_val = class_ranges[i]
            new_val = class_values[i]
            reclassified_data[(raster_data >= min_val) & (raster_data <= max_val)] = new_val

        # Get metadata from the input raster
        meta = src.meta

    # Write the reclassified raster to output file
    with rasterio.open(output_file, 'w', **meta) as dst:
        dst.write(reclassified_data, 1)

    return reclassified_data

def plot_and_save_reclassified(data, output_plot_path):
    # Plot the reclassified data
    plt.figure(figsize=(10, 8))
    img = plt.imshow(data, cmap="Greens", interpolation="none")
    cbar = plt.colorbar(img, label="Value", shrink=0.5)

    # Remove values along the axes
    plt.xticks([])
    plt.yticks([])

    # Add title and adjust layout
    plt.title("Class Fitness") # change title according to use case
    plt.tight_layout()

    # Save the plot
    plt.savefig(output_plot_path, format='png', dpi=300)
    print(f"Plot saved to: {output_plot_path}")

    # Show the plot
    plt.show()

"""
# Example usage:
input_raster_file = "../data/input_raster.tif" # change input path according to use case
output_raster_file = "../clean_data/output_raster.tif" # change output path according to use case
output_plot_path = "../plots/climate_reclass.png" # change plot path according to use case

# Define reclassification parameters
num_classes = 6 # set the number of the new classes
class_ranges = [(0, 3), (4, 7), (8, 16), (17, 28), (29, 30), (31, 255)] # set the range of each class acccording to og vals
class_values = [3, 6, 7, 7, 8, 0] # assign new values to each new class

# Call the function to perform reclassification
reclassified_data = reclassify_raster(input_raster_file, output_raster_file, num_classes, class_ranges, class_values)

# Plot and save the reclassified data
plot_and_save_reclassified(reclassified_data, output_plot_path)
"""