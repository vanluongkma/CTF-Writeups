from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("dataset", exist_ok=True)
image_size = (25, 25)

font = ImageFont.truetype("arial.ttf", 18)

printable_chars = [chr(i) for i in range(32, 127)] + [chr(i) for i in range(160, 256)]

for char in printable_chars:
    font = ImageFont.truetype("arial.ttf", 18)
    image = Image.new("L", image_size, "black")
    draw = ImageDraw.Draw(image)
    x, y, w, h = font.getbbox(char)
    draw.text((5, 1), char, fill="white", font=font)
    image_path = os.path.join("dataset", f"{ord(char)}.png")
    image.save(image_path)
