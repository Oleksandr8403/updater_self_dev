import os
import hashlib
import zipfile
import json


def create_file_hash_and_archive(initial_directory, end_zip_directory):
    hashes = {}
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
            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                zipf.write(file_path, relative_file_path)

    return hashes


# Paths to directories
source_directory = 'D:\\client_game\\'
zip_directory = 'D:\\files_zip\\client_zip'
file_hashes = create_file_hash_and_archive(source_directory, zip_directory)

# Saving hashes to a JSON file
with open('D:\\files_zip\\files_hash.json', 'w') as json_file:
    json.dump(file_hashes, json_file, indent=4)
