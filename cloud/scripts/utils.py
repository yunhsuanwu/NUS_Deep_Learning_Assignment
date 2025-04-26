import os
from typing import List, Tuple, Union
from PIL import Image
import numpy as np


def get_filenames(input_dir: str) -> List[str]:
    """
    Get the list of image filenames from the input directory.
    Args:
        input_dir (str): Directory containing the images.
    Returns:
        List[str]: List of image filenames.
    """
    filenames = []
    for fname in os.listdir(input_dir):
        if fname.endswith((".png", ".jpg", ".jpeg")):
            filenames.append(os.path.join(input_dir, fname))
    return filenames



def load_image(
        path: str,
        crop: Tuple[int, int, int, int] = None,
        convert: str = "RGB") -> Union[np.ndarray, None]:
    """
    Load an image from the given path and convert it to a numpy array.
    Args:
        path (str): Path to the image.
        crop (Tuple[int, int, int, int]): Coordinates for cropping (left, upper, right, lower).
        convert (str): Color mode to convert the image to (default is "RGB").
    Returns:
        np.ndarray: Numpy array of the image.
    """
    try:
        with Image.open(path) as img:
            img = img.convert(convert)
            if crop is not None:
                img = img.crop(crop)
            return np.array(img)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None



def patchify(
        img: np.ndarray,
        patch_size: Tuple[int, int] = (256, 256)) -> List[np.ndarray]:
    """
    Patchify the image into patches of size patch_sizes.
    Args:
        img (np.ndarray): The image to patchify.
        patch_sizes (Tuple[int, int]): The size of the patches.
    Returns:
        List[np.ndarray]: A list of patches.
    """
    patches = []
    h, w = img.shape
    patch_h, patch_w = patch_size

    for i in range(0, h, patch_h):
        for j in range(0, w, patch_w):
            patch = img[i:i+patch_h, j:j+patch_w]
            if patch.shape[0] == patch_h and patch.shape[1] == patch_w:
                patches.append(patch)
    return patches

def save_patches(
        patches: List[np.ndarray], 
        input_file: str,
        output_dir: str) -> None:
    """Save the synthetic clouds to the output directory.
    Args:
        patches: The list of patches.
        output_dir: The output directory.
        starting_index: The starting index for naming the files.
    Returns:
        None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(input_file))[0]

    for idx, patch in enumerate(patches):
        patch_img = Image.fromarray(patch)
        patch_filename = f"{base_name}_patch_{idx}.png"
        patch_img.save(os.path.join(output_dir, patch_filename))