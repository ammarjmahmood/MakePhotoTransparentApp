from PIL import Image, ImageDraw

def create_icon():
    # Create a 512x512 image with transparent background
    img = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a camera-like icon
    # Outer circle
    draw.ellipse((50, 50, 462, 462), fill=(255, 255, 255, 200))
    # Inner circle
    draw.ellipse((100, 100, 412, 412), fill=(0, 0, 0, 0))
    # Lens
    draw.ellipse((200, 200, 312, 312), fill=(255, 255, 255, 150))
    
    # Save the icon
    img.save('icon.png')

if __name__ == '__main__':
    create_icon() 