"""Configuration settings for the game updater application, including server URLs, local directories, and executable
names. Used to centralize settings for easy maintenance and updates."""

version_str = "Updater ver. 1.0 - data"

# URLs for the update server - used to fetch update hashes and zip files
update_server_url = 'http://example_domain/upd/files_la2_hash.json'  # URL for the hash file
zip_base_url = 'http://example_domain/upd/clients_zip/'  # URL for the zip archives

# URL for an image shown in the updater UI
image_url = "https://example_domain/img/update.jpg"

# Entry to be added to the hosts file - can redirect domain names for testing or routing purposes
new_line = "ip example_domain"

# file hash configs
source_directory = 'C:\\client_game\\'

zip_directory = 'C:\\files_zip_srv\\clients_zip'  # Directory to store zipped archives of game files
json_file_path = 'C:\\files_zip_srv\\files_hash.json'  # Path to store the JSON file with hashes of game files

# Executable settings - names and locations within the client directory
play_exe = 'play.exe'  # The main executable for the game
sub_directory_in_client_loc = 'system'  # Subdirectory for localized game files
sub_directory_in_client_en = 'systemen'  # Subdirectory for English game files
