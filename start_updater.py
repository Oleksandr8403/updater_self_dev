import customtkinter as ctk
from tkinter import messagebox, Label, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import logging
import ctypes
import sys
import threading
import os
from game_updater_class import GameUpdater
from start_and_host import add_entry_to_hosts, add_entry_to_hosts_en
from config_example import update_server_url, zip_base_url, image_url, version_str

"""Graphical user interface for the game updater. Allows users to check for updates, apply them, and launch the game 
with or without modifications to the hosts file for language options."""


logger_enabled = False  # Flag to enable or disable logging

# Setting up the logger with specified format and file
if logger_enabled:
    logging.basicConfig(level=logging.DEBUG, filename='updater_tech.log', filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    # Configuring the logger to ignore all messages if logger_enabled is False
    logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)
if logger_enabled:
    logger.info("Script started")

is_updating = False  # Global flag

# Determine the directory of the game based on whether the application is frozen (compiled) or not
if getattr(sys, 'frozen', False):
    # The application is frozen
    game_dir = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    game_dir = os.path.dirname(os.path.abspath(__file__))


# Create an instance of GameUpdater
updater = GameUpdater(game_dir, update_server_url, zip_base_url)


if logger_enabled:
    logger.info("Starting updater...")

# Check for administrative rights and request them if not present
access = updater.is_admin()
if access:
    if logger_enabled:
        logger.info("Running as admin.")
else:
    if logger_enabled:
        logger.info("Not running as admin, requesting admin rights...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    if logger_enabled:
        logger.info("Script re-run requested with admin rights.")
    sys.exit()


# Main function to check for and apply updates
def main_function():
    # Check for updates and apply them if any are found.
    global is_updating
    updates_required = updater.check_for_updates()
    if updates_required:
        updater.download_and_update_files(updates_required, update_progress)
        messagebox.showinfo("State update", "Game client was updated successfully.")
        is_updating = False
        sys.exit()
    else:
        update_progress_bar_final()
        messagebox.showinfo("State update", "Update do not require. You have actual version of game client.")
        is_updating = False
        sys.exit()


def run_updater():
    # Wrapper function to start the update process in a new thread.
    global is_updating
    update_progress_bar_initial()
    if is_updating:
        messagebox.showinfo("State update", "You already started update process. Wait please.")
        return  # Skip if the update is already in progress

    is_updating = True  # Set the flag to True before starting the process
    threading.Thread(target=main_function, daemon=True).start()
    # messagebox.showinfo("path dir", game_dir)
    messagebox.showinfo("State update", "You started update process, it require 5-30 minute,"
                                        " you will be informed at the end...")


def download_and_resize_image(url, new_width, new_height):
    # Download an image from the URL and resize it.
    response = requests.get(url)
    response.raise_for_status()
    img_orig = Image.open(BytesIO(response.content))
    img_resized = img_orig.resize((new_width, new_height))
    return ImageTk.PhotoImage(img_resized)


# Setup the GUI window using customtkinter and tkinter...
# Creating the main window
app = ctk.CTk()
app.title(version_str)

# Setting the window size
window_width = 630
window_height = 400

# Getting the screen size
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculating x and y coordinates to position the window in the center
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2) - int(screen_height / 10)

# Setting the window size and its initial position
app.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
app.resizable(False, False)  # Making the window size fixed (non-resizable)

# Creating buttons using customtkinter
start_button = ctk.CTkButton(app, text="Start game", command=add_entry_to_hosts, font=("Arial", 14),
                             text_color="black", fg_color="orange")
start_button_en = ctk.CTkButton(app, text="Start game in English", command=add_entry_to_hosts_en, font=("Arial", 14),
                                fg_color="green")
update_button = ctk.CTkButton(app, text="Update client game", command=run_updater, font=("Arial", 14))

# Placing the buttons on the same row, but different columns
start_button.grid(row=0, column=1, pady=20, padx=10, sticky="nsew")
start_button_en.grid(row=0, column=0, pady=20, padx=10, sticky="nsew")
update_button.grid(row=0, column=2, pady=20, padx=10, sticky="nsew")

# Adjusting grid column configuration to ensure buttons fit within the window width
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

# Downloading and displaying the image
img = download_and_resize_image(image_url, 600, 280)
img_label = Label(app, image=img)
img_label.grid(row=3, columnspan=3, padx=10, pady=10)

# Creating and placing the progress bar
progress_bar = ttk.Progressbar(app, orient='horizontal', length=550, mode='determinate')
progress_bar.grid(row=2, columnspan=3, padx=(5, 10), pady=1)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)


def update_progress_bar_initial():
    progress_bar['value'] = 2
    progress_bar['maximum'] = 100
    app.update_idletasks()


def update_progress_bar_final():
    progress_bar['value'] = 100
    progress_bar['maximum'] = 100
    app.update_idletasks()


def update_progress(current, total):
    progress_bar['maximum'] = total
    progress_bar['value'] = current
    app.update_idletasks()


# Starting the main loop
app.mainloop()
