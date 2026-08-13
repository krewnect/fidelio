import sys
from PIL import Image

def process_logo(input_path, out_purple, out_white):
    img = Image.open(input_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    # The background color is purple
    bg_r, bg_g, bg_b = 88, 28, 184
    # The Fidelio brand color they want for the purple letters
    fidelio_purple = (91, 14, 184)

    img_white = Image.new("RGBA", (width, height))
    img_purple = Image.new("RGBA", (width, height))
    pixels_w = img_white.load()
    pixels_p = img_purple.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # The face and letters are WHITE.
            # We calculate how "white" the pixel is compared to the purple background.
            # White is 255, 255, 255.
            # Purple is ~ 88, 28, 184.
            # The G channel has the biggest difference (255 - 28 = 227).
            
            diff = g - bg_g
            if diff <= 10:
                alpha = 0.0
            else:
                alpha = min(1.0, diff / 150.0)
            
            # Smooth it
            alpha = alpha ** 1.2
            
            a_val = int(alpha * 255)

            # White version (white letters on transparent background)
            pixels_w[x, y] = (255, 255, 255, a_val)

            # Purple version (purple letters on transparent background)
            pixels_p[x, y] = (fidelio_purple[0], fidelio_purple[1], fidelio_purple[2], a_val)

    # Crop
    bbox = img_white.getbbox()
    if bbox:
        padding = 10
        bbox = (max(0, bbox[0]-padding), max(0, bbox[1]-padding), min(width, bbox[2]+padding), min(height, bbox[3]+padding))
        img_white = img_white.crop(bbox)
        img_purple = img_purple.crop(bbox)

    img_white.save(out_white)
    img_purple.save(out_purple)

if __name__ == "__main__":
    process_logo(sys.argv[1], sys.argv[2], sys.argv[3])
