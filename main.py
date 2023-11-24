import requests
import os
import zipfile
import hashlib
import ctypes
import sys
from pathlib import Path
import logging
import datetime

# Setting up the logger
logging.basicConfig(level=logging.DEBUG, filename='updater_log.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Writing the script start time
logger.info(f"Script started at {datetime.datetime.now()}")  # double time label, require fix!


class GameUpdater:
    def __init__(self, game_dir, update_server_url):
        """ Game updater initialization """
        self.game_dir = Path(game_dir)
        self.update_server_url = update_server_url
        self.backup_dir = self.game_dir / 'backup'
        self.logger = self.setup_logger()

    def is_admin(self):
        try:
            isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
            self.logger.info(f"is_admin: {isAdmin}")
            return isAdmin
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
        url = 'http://example.domen/upd_pn/files_hash.json'
        response = requests.get(url)
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

    def download_and_update_files(self, updates_required_3):
        """ Downloading and installing updates """
        base_url = 'http://example.domen/upd_pn/clients_zip/'
        for file, server_hash in updates_required_3.items():
            formatted_file = file.replace('\\', '/')
            zip_url = base_url + formatted_file + '.zip'
            response = requests.get(zip_url)
            response.raise_for_status()

            # Creating necessary directories before saving the file
            zip_path = os.path.join(self.game_dir, file + '.zip')
            os.makedirs(os.path.dirname(zip_path), exist_ok=True)

            # Saving the zip file
            with open(zip_path, 'wb') as zip_file:
                zip_file.write(response.content)

            # Checking the integrity of the file
            # if self.verify_download(zip_path, server_hash):
            #    # Unpacking the archive
            #    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            #        zip_ref.extractall(self.game_dir)

                # Deleting the zip file after unpacking
            #    os.remove(zip_path)
            # else:
            #    self.logger.error(f"File verification failed for {file}.")

            # Unpacking the archive
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.game_dir)

            # Deleting the zip file after unpacking
            os.remove(zip_path)

            # Logging successful download and installation of the file
            self.logger.info(f"Successfully downloaded and installed {file}")

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

    def update(self):
        """ Starting the update process """
        try:
            self.logger.info("Checking for updates...")
            updates_required_1 = self.check_for_updates()

            if updates_required_1:
                self.logger.info("Updates found. Starting download and installation.")
                # self.backup_files()
                self.download_and_update_files(updates_required_1)
                self.logger.info("Update installed successfully.")
            else:
                self.logger.info("No updates available. Your software is up to date.")
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
            # self.rollback_update()
            raise


if __name__ == "__main__":
    updater = GameUpdater('D:\\client\\', 'http://example.domen/upd_pn/files_hash.json')

    logger.info("Starting updater...")
    access = updater.is_admin()
    if access:
        logger.info("Running as admin.")
        updates_required = updater.check_for_updates()
        if updates_required:
            updater.download_and_update_files(updates_required)
    else:
        logger.info("Not running as admin, requesting admin rights...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        logger.info("Script re-run requested with admin rights.")
        sys.exit()
