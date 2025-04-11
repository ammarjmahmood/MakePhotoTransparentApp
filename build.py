import os
import sys
import subprocess
import requests
import winreg
from pathlib import Path

def download_model():
    """Download the U2Net model if not present."""
    model_path = Path("u2net.onnx")
    if model_path.exists():
        return True
    
    print("Downloading U2Net model...")
    url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(model_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for data in response.iter_content(chunk_size=4096):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50 * downloaded / total_size)
                    sys.stdout.write('\r[{}{}]'.format('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()
        print("\nModel downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading model: {e}")
        return False

def check_inno_setup():
    """Check if Inno Setup is installed and return its path."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                          r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1") as key:
            return winreg.QueryValueEx(key, "InstallLocation")[0]
    except WindowsError:
        return None

def install_inno_setup():
    """Download and install Inno Setup."""
    print("Downloading Inno Setup...")
    url = "https://files.jrsoftware.org/is/6/innosetup-6.2.2.exe"
    setup_path = "innosetup.exe"
    
    try:
        response = requests.get(url)
        with open(setup_path, 'wb') as f:
            f.write(response.content)
        
        print("Installing Inno Setup...")
        subprocess.call([setup_path, '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART'])
        os.remove(setup_path)
        return True
    except Exception as e:
        print(f"Error installing Inno Setup: {e}")
        return False

def create_icon():
    """Create the application icon."""
    print("Creating application icon...")
    try:
        import create_icon
        create_icon.create_icon()
        return True
    except Exception as e:
        print(f"Error creating icon: {e}")
        return False

def build_exe():
    """Build the executable using PyInstaller."""
    try:
        # Install required packages
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        
        # Download the model
        if not download_model():
            print("Failed to download model. Aborting build.")
            return False
        
        # Create icon
        if not create_icon():
            print("Failed to create icon. Aborting build.")
            return False
        
        # Build the executable
        print("\nBuilding executable...")
        subprocess.check_call([
            "pyinstaller",
            "--onefile",
            "--add-data", "u2net.onnx;.",
            "--name", "transparent_bg",
            "--icon", "icon.ico",
            "transparent_bg_app.py"
        ])
        
        # Check/Install Inno Setup
        inno_path = check_inno_setup()
        if not inno_path:
            print("Inno Setup not found. Installing...")
            if not install_inno_setup():
                print("Failed to install Inno Setup. Aborting build.")
                return False
            inno_path = check_inno_setup()
        
        # Create installer
        print("\nCreating installer...")
        iscc = os.path.join(inno_path, "ISCC.exe")
        subprocess.check_call([iscc, "installer.iss"])
        
        print("\nBuild completed successfully!")
        print("\nYou can find the installer at: installer/BackgroundRemover_Setup.exe")
        
        return True
        
    except Exception as e:
        print(f"Error building executable: {e}")
        return False

if __name__ == "__main__":
    build_exe() 