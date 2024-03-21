import requests
import os
import zipfile
import hashlib
import ctypes
from pathlib import Path
import logging
import shutil
import traceback


class GameUpdater:
    def __init__(self, game_dir, server_url_json, server_url_zip_files):
        """ Game updater initialization """
        self.game_dir = Path(game_dir)
        self.server_url_json = server_url_json
        self.server_url_zip_files = server_url_zip_files
        self.backup_dir = self.game_dir / 'backup'
        self.logger = self.setup_logger()

    def is_admin(self):
        try:
            is_admin_right = ctypes.windll.shell32.IsUserAnAdmin()
            self.logger.info(f"is_admin: {is_admin_right}")
            return is_admin_right
        except Exception as e:
            self.logger.error(f"is_admin check failed: {e}")
            return False

    def setup_logger(self):
        """ Setting up the updater's logging actions """
        logger = logging.getLogger('GameUpdater')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(self.game_dir / 'updater.log', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def fetch_server_hashes(self):
        """ Fetching hashes from the server """
        response = requests.get(self.server_url_json)
        response.raise_for_status()
        return response.json()

    def check_for_updates(self):
        """ Checking for updates """
        server_hashes = self.fetch_server_hashes()
        local_hashes = self.get_local_file_hashes()

        updates_required_2 = {}
        for file, server_hash in server_hashes.items():
            if local_hashes.get(file) != server_hash:
                updates_required_2[file] = server_hash

        return updates_required_2

    def download_and_update_files(self, updates_required, update_progress_callback):
        """ Downloading and installing updates """
        temp_dir = os.path.join(self.game_dir, 'temp')  # Temp directory
        total_files = len(updates_required)
        completed_files = 0

        try:
            # Create the temp directory before starting the update process
            os.makedirs(temp_dir, exist_ok=True)

            for file, server_hash in updates_required.items():
                formatted_file = file.replace('\\', '/')
                zip_url = self.server_url_zip_files + formatted_file + '.zip'
                response = requests.get(zip_url)
                response.raise_for_status()

                zip_temp_path = os.path.join(temp_dir, os.path.basename(file) + '.zip')  # Temp path for zip

                # Saving the zip file to the temp directory
                with open(zip_temp_path, 'wb') as zip_file:
                    zip_file.write(response.content)

                # Extracting the zip file
                with zipfile.ZipFile(zip_temp_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Correctly generate the path for the extracted file
                extracted_file_path = os.path.join(temp_dir, file)

                if self.verify_download(extracted_file_path, server_hash):
                    final_file_path = os.path.join(self.game_dir, file)
                    os.makedirs(os.path.dirname(final_file_path), exist_ok=True)
                    os.replace(extracted_file_path, final_file_path)
                    self.logger.info(f"Successfully downloaded and installed {file}")
                    completed_files += 1
                    update_progress_callback(completed_files, total_files)
                    self.logger.info(f"Updated {completed_files} of {total_files}")
                else:
                    self.logger.error(f"File verification failed for {file}")

                # Cleaning up the zip file
                os.remove(zip_temp_path)

        except Exception as e:
            self.logger.error(f"Error during update process: {e}")
            self.logger.debug(traceback.format_exc())

        finally:
            # Cleaning up the temp directory after all updates
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def verify_download(self, file_path, expected_hash):
        """ Verifying the integrity of the downloaded file """
        hash_sha256 = hashlib.sha256()

        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            file_hash = hash_sha256.hexdigest()

            return file_hash == expected_hash
        except IOError as e:
            self.logger.error(f"Error reading file for verification: {e}")
            return False

    def get_local_file_hashes(self):
        """ Creating a dictionary of local file hashes """
        local_hashes = {}
        for root, dirs, files in os.walk(self.game_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_file_path = os.path.relpath(file_path, self.game_dir)

                # Calculating the file hash
                hash_sha256 = hashlib.sha256()
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                file_hash = hash_sha256.hexdigest()
                local_hashes[relative_file_path] = file_hash

        return local_hashes
