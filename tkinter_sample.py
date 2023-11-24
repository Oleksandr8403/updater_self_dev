import tkinter as tk
from tkinter import messagebox


def check_for_updates():
    # Here, call the function to check for updates
    messagebox.showinfo("Check update", "Checking update now...")


def update_software():
    # Here, call the update function
    messagebox.showinfo("Update", "Updating now...")


# Creating the main window
root = tk.Tk()
root.title("Updater")

# Setting the window size
window_width = 300
window_height = 300

# Getting the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculating x and y coordinates to position the window in the center
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2) - int(screen_height / 5)

# Setting the window size and its initial position
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Creating buttons
check_button = tk.Button(root, text="Check update", command=check_for_updates)
update_button = tk.Button(root, text="Update", command=update_software)

# Placing the buttons
check_button.pack()
update_button.pack()

# Starting the main loop
root.mainloop()
