import os
import re

# Folder where your files are stored
folder_path = "/Users/rui/Documents/GitHub/MobileSafety/instagram_ui_recordings"  # <<<---- change this to your folder

# Collect all files matching pattern
files = [f for f in os.listdir(folder_path) if f.startswith("instagram_")]

# Map base numbers to associated files
file_groups = {}
for filename in files:
    match = re.match(r"instagram_(\d+)\.(html|xml|png|json)", filename)
    if match:
        number = int(match.group(1))
        ext = match.group(2)
        if number not in file_groups:
            file_groups[number] = {}
        file_groups[number][ext] = filename

# Sort groups by original number
sorted_groups = sorted(file_groups.items())

# Renaming
for new_index, (old_number, files_dict) in enumerate(sorted_groups, start=1):
    for ext, old_filename in files_dict.items():
        new_filename = f"instagram_{new_index}.{ext}"
        old_path = os.path.join(folder_path, old_filename)
        new_path = os.path.join(folder_path, new_filename)
        print(f"Renaming {old_filename} -> {new_filename}")
        os.rename(old_path, new_path)
