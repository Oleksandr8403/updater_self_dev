import os
import sys
import subprocess
from config_example import new_line, play_exe, sub_directory_in_client_loc, sub_directory_in_client_en

"""Script to modify the Windows hosts file to include a specific entry and then launch the game's executable. Ensures 
the game connects to the designated server."""


def add_entry_to_hosts():
    # Path to the hosts file in Windows systems
    hosts_file = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
    line_exists = False

    # Check if the entry already exists in the hosts file
    with open(hosts_file, 'r') as file:
        for line in file:
            if line.strip() == new_line:
                line_exists = True
                break

    # If the entry does not exist, add it to the hosts file
    if not line_exists:
        with open(hosts_file, 'a') as file:
            file.write(f"{new_line}\n")

    # Construct the path to the game's executable and launch it
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    play_exe_path = os.path.join(current_directory, sub_directory_in_client_loc, play_exe)
    subprocess.Popen([play_exe_path])


def add_entry_to_hosts_en():
    # This function is similar to add_entry_to_hosts but uses the English subdirectory for the game executable
    hosts_file = os.path.join(os.environ['WINDIR'], 'System32', 'drivers', 'etc', 'hosts')
    line_exists = False

    with open(hosts_file, 'r') as file:
        for line in file:
            if line.strip() == new_line:
                line_exists = True
                break

    if not line_exists:
        with open(hosts_file, 'a') as file:
            file.write(f"{new_line}\n")

    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    play_exe_path = os.path.join(current_directory, sub_directory_in_client_en, play_exe)
    subprocess.Popen([play_exe_path])
