# Make Photo Transparent

A cross-platform desktop application for removing backgrounds from images using AI. This project combines the power of [backgroundremover](https://github.com/nadermx/backgroundremover) with a user-friendly desktop interface.

## Features

* Easy-to-use desktop interface for removing image backgrounds
* AI-powered background removal using U2Net model
* Drag and drop interface for images
* Batch processing support
* Cross-platform support (macOS and Windows)
* Preview of results before saving
* Export to PNG with transparency

## Installation

### Prerequisites

* Python 3.8 or higher
* 2GB RAM minimum (4GB recommended)
* 500MB disk space

### macOS

1. Clone the repository:
```bash
git clone https://github.com/ammarjmahmood/MakePhotoTransparent.git
cd MakePhotoTransparent
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python transparent_bg_app.py
```

### Windows

#### Option 1: Using the Installer (Recommended)
1. Download the latest release from the Releases page
2. Run the installer and follow the installation wizard
3. Launch the application from the Start Menu or desktop shortcut

#### Option 2: From Source
1. Clone the repository:
```bash
git clone https://github.com/ammarjmahmood/MakePhotoTransparent.git
cd MakePhotoTransparent
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python transparent_bg_app.py
```

## Usage

1. Launch the application
2. Drag and drop images onto the application window
3. Click "Remove Background" to process the image
4. Preview the result
5. Save the processed image with a transparent background

## Building from Source

### macOS
```bash
python build.py
```

### Windows
```bash
.\windows_build.bat
```

## Credits

This project builds upon the following open-source projects:

* [backgroundremover](https://github.com/nadermx/backgroundremover) by Johnathan Nader - Core background removal functionality
* [U-2-Net](https://github.com/NathanUA/U-2-Net) - Deep learning model for salient object detection

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

* Thanks to the [backgroundremover](https://github.com/nadermx/backgroundremover) team for their excellent base library
* Thanks to the U-2-Net team for their amazing AI model