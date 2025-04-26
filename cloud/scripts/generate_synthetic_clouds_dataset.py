import os
from typing import List, Tuple
import numpy as np
from PIL import Image
from tqdm import tqdm
import argparse
import noise
from utils import load_image, patchify, save_patches, get_filenames


def build_argparser() -> argparse.ArgumentParser:
    """
    Build the argument parser for command line arguments.
    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description="Process real clouds dataset.")
    parser.add_argument(
        "--input_dir", type=str, required=True,
        help="Directory containing the images to process."
    )
    parser.add_argument(
        "--input_mask", type=str, required=True,
        help="Directory containing the mask."
    )
    parser.add_argument(
        "--patch_size", type=int, nargs=2, required=True,
        help="Size of the patches (height, width)."
    )
    parser.add_argument(
        "--crop", type=int, nargs=4, required=True,
        help="Coordinates for cropping (left, upper, right, lower)."
    )
    parser.add_argument(
        "--output_dir", type=str, required=True,
        help="Directory to save the patches."
    )
    parser.add_argument(
        "--max_files", type=int, default=-1,
        help="Maximum number of files to process. Default is -1 (all files)."
    )
    return parser


def generate_synthetic_clouds(
        shape: Tuple[int, int],
        res: Tuple[int, int],
        octaves: int) -> np.ndarray:
    """Generate a 2D numpy array of noise.
    Args:
        shape: The shape of the generated array (tuple of two ints).
            This must be a multiple of res.
        res: The number of periods of noise to generate along each
            axis (tuple of two ints). Note shape must be a multiple of
            res.
        octaves: The number of octaves in the noise.
    Returns:
        A numpy array of shape shape with the generated noise.
    """
    h, w = shape
    scale_x = w / res[0]
    scale_y = h / res[1]

    noise_map = np.zeros((h, w), dtype=np.float32)

    for i in range(h):
        for j in range(w):
            x = j / scale_x
            y = i / scale_y
            value = noise.pnoise2(x, y, octaves=octaves)
            noise_map[i][j] = value

    noise_map = ((noise_map + 1) / 2 * 255).astype(np.uint8)
    return noise_map



def apply_synthetic_clouds_to_mask(
        noise: np.ndarray,
        mask: np.ndarray) -> np.ndarray:
    """Apply the generated noise to the mask. First, normalize the
    noise to be between 0 and 255, then add the noise to the mask.
    The mask is assumed to be in the range [0, 255]. Clip the output
    to be in the range [0, 255] and convert it to uint8.
    Args:
        noise: The generated noise.
        mask: The mask to apply the noise to.
    Returns:
        A numpy array of the same shape as the mask with the noise
        applied.
    """
    result = noise.copy()
    result[mask == 255] = 255 
    return result.astype(np.uint8)



def process(
        N: int, 
        input_mask: str,
        patch_size: Tuple[int, int],
        crop: Tuple[int, int, int, int],
        output_dir: str) -> None:
    """
    Process the real clouds by loading the images, patchifying them,
    and saving the patches to the output directory.
    Args:
        N (int): Number of images to process.
        input_mask (str): Path to the input mask.
        patch_size (Tuple[int, int]): Size of the patches (height, width).
        crop (Tuple[int, int, int, int]): Coordinates for cropping (left, upper, right, lower).
        output_dir (str): Directory to save the patches.
    Returns:
        None
    """
    mask = load_image(input_mask, crop=crop, convert="L")
    if mask is None:
        print("Failed to load mask.")
        return

    for i in tqdm(range(N), desc="Generating synthetic clouds"):
        noise = generate_synthetic_clouds(mask.shape, res=(4, 4), octaves=6)
        combined = apply_synthetic_clouds_to_mask(noise, mask)
        patches = patchify(combined, patch_size)

        patches_rgb = [np.stack([p]*3, axis=-1) for p in patches]
        save_patches(patches_rgb, f"synthetic_{i}", output_dir)


def main():
    """
    Main function to execute the script.
    """
    parser = build_argparser()
    args = parser.parse_args()
    filenames = get_filenames(args.input_dir)
    if args.max_files > 0:
        filenames = filenames[:args.max_files]
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    process(len(filenames), args.input_mask, args.patch_size, args.crop, args.output_dir)


if __name__ == "__main__":
    main()
