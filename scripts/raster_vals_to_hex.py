import geopandas as gpd
import rasterio
import rasterio.mask
import numpy as np

def assign_raster_values_to_hexagons(hexagon_file, raster_file, output_column):
    # Load the hexagon GeoJSON file
    hexagons = gpd.read_file(hexagon_file)
    print(f"Number of hexagons: {len(hexagons)}")
    print(f"Hexagon CRS: {hexagons.crs}")

    # Open the raster file
    with rasterio.open(raster_file) as src:
        print(f"Raster CRS: {src.crs}")

        # Initialize a list to store the results
        results = []

        # Loop through each hexagon
        for _, hexagon in hexagons.iterrows():
            # Mask the raster with the hexagon
            out_image, _ = rasterio.mask.mask(src, [hexagon.geometry], crop=True)

            # Print out the raster values within the hexagon
            print(out_image)

            # Print the unique values and their counts
            unique, counts = np.unique(out_image, return_counts=True)
            print(dict(zip(unique, counts)))

            # Calculate the average value of the raster within the hexagon
            avg_val = np.nanmean(out_image)

            # Append the result to the list
            results.append(avg_val)

        # Assign the results to the specified column in the hexagon GeoDataFrame
        hexagons[output_column] = results

    # Save the GeoDataFrame to a new GeoJSON file
    hexagons.to_file(hexagon_file, driver='GeoJSON')