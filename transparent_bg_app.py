import os
import sys
import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image
import winreg
import ctypes
from pathlib import Path

def remove_background(input_path, threshold=0.5, refinement=True):
    """Remove background from an image using U2Net model."""
    try:
        # Get output path
        filename = os.path.basename(input_path)
        filename_no_ext = os.path.splitext(filename)[0]
        output_dir = os.path.dirname(input_path)
        output_path = os.path.join(output_dir, f"{filename_no_ext}_transparent.png")
        
        # Load model
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, "u2net.onnx")
        if not os.path.exists(model_path):
            show_error("Model not found", "Please ensure u2net.onnx is in the same directory as the script.")
            return None
        
        # Show processing notification
        show_notification("Processing", f"Removing background from {filename}...")
        
        model = ort.InferenceSession(model_path)
        
        # Load and preprocess image
        input_image = cv2.imread(input_path)
        original_h, original_w = input_image.shape[:2]
        
        # Resize for model input
        resized_image = cv2.resize(input_image, (320, 320))
        blob = cv2.dnn.blobFromImage(resized_image, 1.0 / 255, (320, 320), (0, 0, 0), swapRB=True)
        
        # Run inference
        inputs = {model.get_inputs()[0].name: blob}
        outputs = model.run(None, inputs)
        mask = outputs[0]
        
        # Postprocess mask
        mask = mask.squeeze()
        mask = cv2.resize(mask, (original_w, original_h))
        mask = np.where(mask > threshold, 255, 0).astype(np.uint8)
        
        # Apply refinement if enabled
        if refinement:
            mask = cv2.GaussianBlur(mask, (5, 5), 0)
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Apply mask to original image
        orig_image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        rgba = cv2.cvtColor(orig_image, cv2.COLOR_BGR2BGRA)
        rgba[:, :, 3] = mask
        
        # Save result
        cv2.imwrite(output_path, rgba)
        show_notification("Success", f"Background removed! Saved as:\n{os.path.basename(output_path)}")
        return output_path
        
    except Exception as e:
        show_error("Error", f"Failed to remove background: {str(e)}")
        return None

def show_notification(title, message):
    """Show a Windows notification."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)

def show_error(title, message):
    """Show a Windows error message."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)

def install_context_menu():
    """Install the context menu entry for image files."""
    try:
        # Get the path to the executable
        if getattr(sys, 'frozen', False):
            # If running as exe (PyInstaller)
            script_path = sys.executable
        else:
            # If running as script
            script_path = os.path.abspath(__file__)
        
        # Create the command
        command = f'"{sys.executable}" "{script_path}" "%1"'
        
        # File types to add the context menu to
        file_types = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        
        for ext in file_types:
            # Add context menu for each file type
            key_path = f'SystemFileAssociations\\{ext}\\shell\\RemoveBackground'
            
            # Create the key
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
            winreg.SetValue(key, '', winreg.REG_SZ, 'Remove Background')
            
            # Add icon (using Windows' photo viewer icon)
            winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, 'imageres.dll,-122')
            
            # Add command
            command_key = winreg.CreateKey(key, 'command')
            winreg.SetValue(command_key, '', winreg.REG_SZ, command)
            
            # Cleanup
            winreg.CloseKey(command_key)
            winreg.CloseKey(key)
        
        show_notification("Success", "Context menu entry installed successfully!")
        return True
        
    except Exception as e:
        show_error("Installation Error", f"Failed to install context menu: {str(e)}")
        return False

def uninstall_context_menu():
    """Remove the context menu entry."""
    try:
        file_types = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
        
        for ext in file_types:
            key_path = f'SystemFileAssociations\\{ext}\\shell\\RemoveBackground'
            try:
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command")
                winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
            except WindowsError:
                pass
        
        show_notification("Success", "Context menu entry removed successfully!")
        return True
        
    except Exception as e:
        show_error("Uninstallation Error", f"Failed to remove context menu: {str(e)}")
        return False

def main():
    # If no arguments provided, install/uninstall context menu
    if len(sys.argv) == 1:
        install_context_menu()
        return
    
    # If --uninstall flag is provided, remove context menu
    if len(sys.argv) == 2 and sys.argv[1] == "--uninstall":
        uninstall_context_menu()
        return
    
    # Otherwise, process the image
    if len(sys.argv) == 2:
        input_path = sys.argv[1]
        if not os.path.exists(input_path):
            show_error("Error", f"File not found: {input_path}")
            return
        
        remove_background(input_path)

if __name__ == "__main__":
    main()
