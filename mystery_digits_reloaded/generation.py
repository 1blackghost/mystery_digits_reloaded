from image_generator.generator import generate_and_get_digits
import uuid
import random
import string
import json

def generate_random_filename(extension='txt', length=8):
    random_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    unique_id = uuid.uuid4()
    filename = f"{random_prefix}_{unique_id}.{extension}"
    return filename

# Create a dictionary to hold the filenames for each level
filenames_by_level = {}

# Loop to generate images and filenames
for i in range(40):  # Levels
    level_filenames = []  # List to hold filenames for this level
    for j in range(15):  # For each level, generate 15 images
        filename = f"{generate_random_filename('jpg')}_{i}.jpg"
        generate_and_get_digits(800, 600, i, filename)  # Generate image with digits
        level_filenames.append(filename)  # Add filename to the list

    # Store the list of filenames for this level in the dictionary
    filenames_by_level[f'level_{i}'] = level_filenames

# Write the filenames to a JSON file
with open("data.json", "w") as json_file:
    json.dump(filenames_by_level, json_file, indent=4)
