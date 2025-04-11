# Transparent Screenshot

A cross-platform tool for taking screenshots with automatic background removal capabilities.

## Features

- Take full-screen or area-selected screenshots
- AI-powered background removal
- System tray integration
- Global keyboard shortcuts
- Save screenshots to a designated folder
- Cross-platform support (macOS and Windows)

## Installation

### Windows

#### Option 1: Using the Installer (Recommended)
1. Download the latest `BackgroundRemover_Setup.exe` from the [Releases](https://github.com/ammarmahmood1999/transparentscreenshot/releases) page
2. Run the installer and follow the installation wizard
3. The application will be installed and shortcuts will be created in the Start Menu
4. Launch the application from the Start Menu or desktop shortcut

#### Option 2: Standalone Executable
1. Download `transparent_bg.exe` from the [Releases](https://github.com/ammarmahmood1999/transparentscreenshot/releases) page
2. Run the executable directly (no installation required)

### macOS

1. Clone the repository:
```bash
git clone https://github.com/ammarmahmood1999/transparentscreenshot.git
cd transparentscreenshot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Generate the app icon:
```bash
python create_icon.py
```

4. Run the application:
```bash
python transparent_bg_app.py
```

## Usage

### Windows
1. After installation, the app will run in the system tray
2. Right-click the tray icon to:
   - Take a full-screen screenshot (or press Win+Shift+4)
   - Take an area screenshot (or press Win+Shift+5)
   - Access settings
   - Exit the application
3. Screenshots are saved to your Pictures folder by default
4. Right-click any saved screenshot to remove its background

### macOS
1. The app runs in the menu bar
2. Use Command+Shift+4 for full-screen screenshots
3. Use Command+Shift+5 for area selection
4. Screenshots are saved to your Desktop by default
5. Right-click any saved screenshot to remove its background

## Building from Source (Windows)

1. Clone the repository:
```bash
git clone https://github.com/ammarmahmood1999/transparentscreenshot.git
cd transparentscreenshot
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the build script:
```bash
.\windows_build.bat
```

This will create:
- Standalone executable at: `dist\transparent_bg.exe`
- Installer at: `installer\BackgroundRemover_Setup.exe`

## Requirements

- Python 3.8 or higher
- Windows 10/11 or macOS 10.15+
- 2GB RAM minimum (4GB recommended)
- 500MB disk space

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.