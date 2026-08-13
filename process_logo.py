import sys
from PIL import Image

def process_logo(input_path, out_purple, out_white):
    img = Image.open(input_path).convert("L")  # Convert to grayscale
    pixels = img.load()
    width, height = img.size

    # Fidelio official purple color
    fidelio_purple = (91, 14, 184) # #5b0eb8

    img_white = Image.new("RGBA", (width, height))
    img_purple = Image.new("RGBA", (width, height))
    pixels_w = img_white.load()
    pixels_p = img_purple.load()

    # Find a good background white level by taking the 95th percentile
    # Just assume anything > 240 is background
    bg_thresh = 240

    for y in range(height):
        for x in range(width):
            val = pixels[x, y]

            # Calculate alpha (darker pixels = more opaque)
            if val >= bg_thresh:
                alpha = 0.0
            else:
                alpha = 1.0 - (val / bg_thresh)
            
            # Non-linear adjustment to make text crispier
            alpha = alpha ** 0.8
            if alpha > 1.0: alpha = 1.0

            a_val = int(alpha * 255)

            # White version
            pixels_w[x, y] = (255, 255, 255, a_val)

            # Purple version
            pixels_p[x, y] = (fidelio_purple[0], fidelio_purple[1], fidelio_purple[2], a_val)

    # Crop out excess transparency
    bbox = img_white.getbbox()
    if bbox:
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
