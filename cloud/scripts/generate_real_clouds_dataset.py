import os
from typing import List, Tuple
from tqdm import tqdm
import argparse
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
        "--crop", type=int, nargs=4, required=True,
        help="Coordinates for cropping (left, upper, right, lower)."
    )
    parser.add_argument(
        "--patch_size", type=int, nargs=2, required=True,
        help="Size of the patches (height, width)."
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


def process(
        filenames: List[str], 
        patch_size: Tuple[int, int],
        crop: Tuple[int, int, int, int],
        output_dir: str) -> None:
    """
    Process the real clouds by loading the images, patchifying them,
    and saving the patches to the output directory.
    Args:
        filenames (List[str]): List of image filenames.
        patch_size (Tuple[int, int]): Size of the patches (height, width).
        crop (Tuple[int, int, int, int]): Coordinates for cropping (left, upper, right, lower).
        output_dir (str): Directory to save the patches.
    Returns:
        None
    """
    from utils import load_image, patchify, save_patches
    import os

    for file in filenames:
        image = load_image(file, crop)
        if image is None:
            print(f"Skipping file due to loading error: {file}")
            continue

        left, top, right, bottom = crop
        image_cropped = image[top:bottom, left:right]
        patches = patchify(image_cropped, patch_size)
        save_patches(patches, file, output_dir)


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
    process(filenames, args.patch_size, args.crop, args.output_dir)


if __name__ == "__main__":
    main()
