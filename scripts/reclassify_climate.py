import numpy as np
import rasterio
import matplotlib.pyplot as plt

def reclassify_and_assign_values(input_path, output_path, czf_values):
    # Open the input GeoTIFF file
    with rasterio.open(input_path) as src:
        # Read the raster data
        data = src.read(1)

        # Reclassify values
        reclassified_data = np.piecewise(data,
                                          [data == 31, (data >= 1) & (data <= 3),
                                           (data >= 4) & (data <= 7), (data >= 8) & (data <= 16),
                                           (data >= 17) & (data <= 28), (data >= 29) & (data <= 30),
                                           (data >= 31) & (data <= 255)],
                                          [czf_values[5], czf_values[0], czf_values[1],
                                           czf_values[2], czf_values[3], czf_values[4], czf_values[5]])

        # Update the metadata for the output file
        kwargs = src.meta
        kwargs.update({
            "driver": "GTiff",
            "count": 1,
            "compress": "lzw",
            "dtype": "float32"
        })

        # Create the output GeoTIFF file
        with rasterio.open(output_path, "w", **kwargs) as dst:
            # Write the reclassified data to the output file
            dst.write(reclassified_data, 1)

        # Plot the reclassified data
    plt.figure(figsize=(10, 8))
    img = plt.imshow(reclassified_data, cmap="Greens", interpolation="none")
    cbar = plt.colorbar(img, label="Fitness", shrink=0.5)

    # Remove values along the axes
    plt.xticks([])
    plt.yticks([])

    # Add title and adjust layout
    plt.title("Climate Zone Fitness")
    plt.tight_layout()

    # Save the plot if save_path is provided
    if save_plot_path:
        plt.savefig(save_plot_path, format='png', dpi=300)
        print(f"Plot saved to: {save_plot_path}")

    # Show the plot after saving
    plt.show()

# File paths relative to the repo
input_tiff_path = "../data/koppen_geiger_1991_2020.tif"
output_tiff_path = "../clean_data/climate_reclass.tif"

# Set climate zone fitness values for each class/climate zone
czf_tropical = 3
czf_dry = 6
czf_temperate = 7
czf_continental = 7
czf_polar = 8
czf_no_val = 0

# Combine the variable values into a list
czf_values = [czf_tropical, czf_dry, czf_temperate, czf_continental, czf_polar, czf_no_val]

# save path to save the plot
save_plot_path = "../plots/climate_reclass.png"

# Call the function to perform reclassification and value assignment
reclassify_and_assign_values(input_tiff_path, output_tiff_path, czf_values)