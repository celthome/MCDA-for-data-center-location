from scripts.reclass_vector_template import reclassify_vector

# Define your parameters
input_file = "../data/clean/clean_natural_hazards.csv"
output_file = "../data/output/natural_hazards_reclass.geojson"
attribute = "Deaths"  # replace with the attribute you want to reclassify
num_classes = 5  # replace with the number of classes you want
class_ranges = [(0, 0), (0, 0.1), (0.1, 0.5), (0.5, 1), (1, float("inf"))]  # replace with your class ranges
class_values = [10, 8, 7, 6, 2]  # replace with your class values

# Call the reclassify_vector function
reclassify_vector(input_file, output_file, attribute, num_classes, class_ranges, class_values)
