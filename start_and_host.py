import os
import sys
import subprocess
from config_example import new_line, play_exe, sub_directory_in_client_loc, sub_directory_in_client_en


def add_entry_to_hosts():
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
    play_exe_path = os.path.join(current_directory, sub_directory_in_client_loc, play_exe)
    subprocess.Popen([play_exe_path])


def add_entry_to_hosts_en():
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
