# Game File Updater

## Overview

After several months of development, I am excited to present the new full version of this updater.

The Game File Updater is an advanced tool designed to streamline the process of keeping your game files synchronized with the latest updates directly from the developers. This utility goes beyond simple file updates; it intelligently checks file integrity through hash comparisons, downloads only the necessary updates, and ensures that your gaming experience is enhanced with the latest features, fixes, and content without manual intervention.

Built with flexibility in mind, designed specifically for online gaming projects, the Game File Updater serves as an essential tool for developers and gaming companies aiming to streamline the update process for their players. By ensuring seamless delivery of the latest game patches and updates directly to the user's system, it enhances the gaming experience and keeps your player base engaged with the most current content and features. If your project seeks to elevate its update mechanism with efficiency and reliability, the Game File Updater is the solution you need.

## Features

- **Automatic File Hash Comparison**: Quickly determines which files need updating by comparing local file hashes against the server's version.
- **Efficient Updates**: Downloads and applies only the necessary updates, saving bandwidth and time.
- **Multi-language Support**: Offers the capability to start the game in different languages by modifying the hosts file accordingly.
- **User-Friendly Interface**: Features a simple and intuitive graphical user interface (GUI) for easy operation by end-users.
- **Extensive Logging**: Maintains detailed logs of all operations, aiding in troubleshooting and ensuring transparency of the update process.
- **Administrative Check**: Ensures the updater runs with the necessary permissions for seamless updates and modifications.

## Getting Started

### Prerequisites

- Python 3.7
- `requests`, `customtkinter`, and `Pillow` libraries installed.
- Administrative privileges on the system for certain operations.

### Installation

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/Oleksandr8403/updater_self_dev.git
   ```
2. Navigate to the project directory:
   ```
   cd updater_self_dev
   ```
3. Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```

## Setting Up the Updater

To successfully install and utilize the Game File Updater for your online game, follow these essential steps:

### Create Hashes and Zip Archives

- **Generate Hashes**: Use the `file_hash.py` script to create SHA256 hashes of all client game files. This script will also automatically zip each file.
- **Create JSON File**: The script outputs a JSON file containing the hashes. This file is crucial for the updater to verify the integrity of each file during the update process.

### Upload Files to Server

- **Upload Zipped Files and JSON**: Once you have your zip files and JSON hash file ready, upload them to a web server or cloud storage service. Ensure this location is accessible over the internet to allow users to download updates.

### Configuration

Edit the `config_example.py` file to set your game directory, server URLs for file hashes and updates, and any other game-specific settings.

### Running the Updater

#### Using Python Script

To start the updater, run the `start_updater.py` script directly with Python:

```bash
python start_updater.py
```

#### Compiling to an Executable File

If you prefer to run the updater as a standalone executable without the need for a Python installation, you can compile the script using PyInstaller. This is particularly useful for distribution or making the updater user-friendly for those unfamiliar with Python.

First, install PyInstaller:

```bash
pip install pyinstaller
```

Then, navigate to the directory containing your script and use PyInstaller to compile it into an executable:

```bash
pyinstaller --onefile --windowed start_updater.py
```

- The `--onefile` flag tells PyInstaller to bundle everything into a single executable.
- The `--windowed` flag prevents a command prompt window from opening when the GUI runs (optional, remove if running a CLI application).

After compilation, you'll find the executable in the `dist` directory within your project folder. You can run this executable directly without needing to execute the Python script or having Python installed.


## Contributing

We welcome contributions from the community! Whether it's adding new features, fixing bugs, or improving documentation, your help is appreciated. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all the contributors who have helped to make this tool better.
- Special thanks to the open-source community for providing the necessary libraries and tools.

---

Feel free to customize the sections according to your project's specific needs, such as adding a section on how to report bugs, request features, or contact the development team for support.