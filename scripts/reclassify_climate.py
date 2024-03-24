"""
Author: Dominik Neumann, Celina Thomé
Takes a given koppen climate zone subtypes geotiff of the world, reclassifies the subtypes into general climate zones.
Manually set "fitness" values for each climate zone. Script creates new geotiff, plots it and saves the plot.
"""

from scripts.reclass_raster_template import reclassify_raster, plot_and_save_reclassified

# Define your parameters
input_raster_file = "../data/koppen_geiger_1991_2020.tif"
output_raster_file = "../clean_data/climate_reclass.tif"
output_plot_path = "../plots/climate_reclass.png"

num_classes = 6 # set the number of the new classes
class_ranges = [(0, 3), (4, 7), (8, 16), (17, 28), (29, 30), (31, 255)] # set the range of each class acccording to og vals
class_values = [3, 6, 7, 7, 8, -9999] # assign new values to each new class

# Call the function to perform reclassification
reclassified_data = reclassify_raster(input_raster_file, output_raster_file, num_classes, class_ranges, class_values)

# Plot and save the reclassified data
plot_and_save_reclassified(reclassified_data, output_plot_path)