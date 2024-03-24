import geopandas as gpd
import matplotlib.pyplot as plt

def reclassify_vector(input_file, output_file, attribute, num_classes, class_ranges, class_values):
    # Load the input vector file
    gdf = gpd.read_file(input_file)

    # Initialize reclassified column with zeros
    gdf['reclassified'] = 0

    # Loop through each class and reclassify the vector
    for i in range(num_classes):
        min_val, max_val = class_ranges[i]
        new_val = class_values[i]
        gdf.loc[(gdf[attribute] >= min_val) & (gdf[attribute] <= max_val), 'reclassified'] = new_val

    # Write the reclassified vector to output file
    gdf.to_file(output_file, driver='GeoJSON')

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