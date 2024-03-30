from scripts.reclass_vector_template import reclassify_vector

# Define your parameters
input_file = "../data/clean/crime_clean.csv"
output_file = "../data/output/crime_reclass.geojson"
attribute = "Resilience"  # replace with the attribute you want to reclassify
num_classes = 10  # replace with the number of classes you want
class_ranges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]  # replace with your class ranges
class_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # replace with your class values; the index means resilience -> positive

# Call the reclassify_vector function
reclassify_vector(input_file, output_file, attribute, num_classes, class_ranges, class_values)