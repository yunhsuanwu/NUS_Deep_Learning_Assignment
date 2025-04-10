from typing import List, Tuple
import os
from pathlib import Path
import argparse


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
        "--A", type=str, required=True,
        help="Directory containing the images of modality A to process."
    )
    parser.add_argument(
        "--B", type=str, required=True,
        help="Directory containing the images of modality B to process."
    )
    parser.add_argument(
        "--folders", type=str, nargs=4, required=True,
        help="List of folder names to create for training and testing data."
    )
    parser.add_argument(
        "--alpha", type=float, required=True,
        help="Ratio of training data to total data."
    )
    return parser


def browse_folder(
        path: Path, 
        A: str, 
        B: str) -> Tuple[List[Path], List[Path]]:
    """
    Browse a directory and return a list of all the png files in it and its subfolder.
    """
    return NotImplementedError


def check_existence(
        filenames: List[Path]) -> None:
    """
    Check if the paths exist.
    Args:
        filenames (List[Path]): List of filenames.
    Returns:
        None
    """
    return NotImplementedError


def create_folders(
        input_dir: Path, 
        folder_list: List[str]) -> None:
    """
    Create folders for training and testing data.
    Args:
        input_dir (Path): Input directory.
        folder_list (List[str]): List of folder names to create.
    Returns:
        None
    """
    return NotImplementedError


def split_train_test(
        filenames: List[Path], 
        alpha: float) -> Tuple[List[Path], List[Path]]:
    """
    Split the filenames into training and testing sets.
    Args:
        filenames (List[Path]): List of filenames.
        alpha (float): Ratio of training data to total data.
    Returns:
        Tuple[List[Path], List[Path]]: Training and testing filenames.
    """
    return NotImplementedError


def create_symlinks(
        filenames: List[Path],
        input_dir: Path,
        split_dir: Path) -> None:
    """
    Create symbolic links for the training and testing images.
    Args:
        filenames (List[Path]): List of filenames.
        input_dir (Path): Input directory.
        split_dir (Path): Split directory.
    Returns:
        None
    """
    return NotImplementedError


def process(input_dir: str, A: str, B: str, folders: List[str], alpha: float) -> None:
    """
    Format the dataset for training and testing.
    Args:
        data_dir (str): Directory containing the images.
        A (str): Name of the first dataset.
        B (str): Name of the second dataset.
        folders (List[str]): List of folder names to create.
        alpha (float): Ratio of training data to total data.
    Returns:
        None
    """
    return NotImplementedError


def main():
    """
    Main function to execute the script.
    """
    parser = build_argparser()
    args = parser.parse_args()

    process(args.input_dir, args.A, args.B, args.folders, args.alpha)


if __name__ == "__main__":
    main()
