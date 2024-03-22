import os
import hashlib
import zipfile
import json
import time
from typing import Dict
from config_example import source_directory, zip_directory, json_file_path

"""Utility script for hashing game files and archiving them into zip files. Generates a JSON manifest of file hashes 
for integrity verification."""


def create_file_hash_and_archive(initial_directory: str, end_zip_directory: str) -> Dict[str, str]:
    # Tracks execution time for the function
    start_time = time.time()
    hashes = {}

    # Walk through the directory structure of the source directory
    for root, dirs, files in os.walk(initial_directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, initial_directory)

            # Calculating the file hash
            hash_sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            file_hash = hash_sha256.hexdigest()
            hashes[relative_file_path] = file_hash

            # Creating the path in the archive directory
            zip_file_path = os.path.join(end_zip_directory, relative_file_path) + '.zip'
            os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

            # Creating the file archive
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=5) as zipf:
                zipf.write(file_path, relative_file_path)

    # Log the execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")

    return hashes


# Create file hashes and archive them
file_hashes = create_file_hash_and_archive(source_directory, zip_directory)

# Save the file hashes to a JSON file for later reference
with open(json_file_path, 'w') as json_file:
    json.dump(file_hashes, json_file, indent=4)
