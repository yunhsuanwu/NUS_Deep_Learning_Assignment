from PIL import Image
import numpy as np
import os

def extract_green_border_mask(input_path, output_path):
    # Open the image and convert to RGB
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img)

    green_mask = (arr[:, :, 1] > 200) & (arr[:, :, 0] < 200) & (arr[:, :, 2] < 200)

    binary_mask = np.where(green_mask, 255, 0).astype(np.uint8)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    Image.fromarray(binary_mask).save(output_path)
    print(f"✅ Mask saved to {output_path}")

extract_green_border_mask("scrape_images/20250201_0000.jpg", "grey_images/grey_20250201_0000.jpg")