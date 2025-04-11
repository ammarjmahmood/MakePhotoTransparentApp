from PIL import Image, ImageDraw

def create_icon():
    # Create a 256x256 image with transparent background
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Define colors
    primary_color = (65, 131, 215)  # Blue
    secondary_color = (255, 255, 255)  # White
    
    # Draw main circle
    margin = size // 8
    draw.ellipse([margin, margin, size - margin, size - margin], 
                fill=primary_color)
    
    # Draw smaller circle for transparency effect
    inner_margin = size // 3
    draw.ellipse([inner_margin, inner_margin, size - inner_margin, size - inner_margin], 
                fill=secondary_color)
    
    # Draw checkered pattern in the inner circle to represent transparency
    checker_size = size // 16
    for i in range(inner_margin, size - inner_margin, checker_size):
        for j in range(inner_margin, size - inner_margin, checker_size):
            if (i + j) % (checker_size * 2) == 0:
                draw.rectangle([i, j, i + checker_size, j + checker_size], 
                             fill=primary_color)
    
    # Save in multiple sizes for the .ico file
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    for s in sizes:
        resized = image.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save as .ico
    images[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes], 
                  append_images=images[1:])
    
    print("Icon created successfully!")

if __name__ == "__main__":
    create_icon() 