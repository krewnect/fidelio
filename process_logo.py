import sys
from PIL import Image

def process_logo(input_path, out_purple, out_white):
    img = Image.open(input_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    # Sample background color from top-left corner
    bg_r, bg_g, bg_b = pixels[0, 0]

    # Create new images
    img_white = Image.new("RGBA", (width, height))
    img_purple = Image.new("RGBA", (width, height))
    pixels_w = img_white.load()
    pixels_p = img_purple.load()

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Calculate alpha based on distance from background to white
            diff_r = 255 - bg_r
            diff_g = 255 - bg_g
            diff_b = 255 - bg_b

            alpha_r = (r - bg_r) / diff_r if diff_r > 0 else 0
            alpha_g = (g - bg_g) / diff_g if diff_g > 0 else 0
            alpha_b = (b - bg_b) / diff_b if diff_b > 0 else 0

            # Average alpha (clamped between 0 and 1)
            alpha = (alpha_r + alpha_g + alpha_b) / 3
            alpha = max(0.0, min(1.0, alpha))
            
            # Since JPEG has compression artifacts, anything very close to background is fully transparent
            if alpha < 0.05:
                alpha = 0.0
            
            # Non-linear adjustment to make text crispier
            alpha = alpha ** 0.8
            if alpha > 1.0: alpha = 1.0

            a_val = int(alpha * 255)

            # White version
            pixels_w[x, y] = (255, 255, 255, a_val)

            # Purple version
            pixels_p[x, y] = (bg_r, bg_g, bg_b, a_val)

    # Crop out excess transparency
    bbox = img_white.getbbox()
    if bbox:
        # Add 20px padding
        padding = 20
        bbox = (
            max(0, bbox[0] - padding),
            max(0, bbox[1] - padding),
            min(width, bbox[2] + padding),
            min(height, bbox[3] + padding)
        )
        img_white = img_white.crop(bbox)
        img_purple = img_purple.crop(bbox)

    img_white.save(out_white)
    img_purple.save(out_purple)
    print(f"Saved {out_white} and {out_purple}")

if __name__ == "__main__":
    process_logo(sys.argv[1], sys.argv[2], sys.argv[3])
