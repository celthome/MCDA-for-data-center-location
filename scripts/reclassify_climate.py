import numpy as np
import rasterio


def reclassify_and_assign_values(input_path, output_path):
    # Open the input GeoTIFF file
    with rasterio.open(input_path) as src:
        # Read the raster data
        data = src.read(1)

        # Reclassify values
        reclassified_data = np.piecewise(data,
                                          [data >= 1, (data >= 4) & (data <= 7),
                                           (data >= 8) & (data <= 16), (data >= 17) & (data <= 28),
                                           (data >= 29) & (data <= 30)],
                                          [1, 2, 3, 4, 5])

        # Assign variable values between 0 and 10
        reclassified_data = np.interp(reclassified_data, [1, 2, 3, 4, 5], [3, 6, 7, 7, 8])

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

# file paths relative to the repo
input_tiff_path = "../data/koppen_geiger_1991_2020.tif"
output_tiff_path = "../clean_data/climate_reclass.tif"

# Call the function to perform reclassification and value assignment
reclassify_and_assign_values(input_tiff_path, output_tiff_path)