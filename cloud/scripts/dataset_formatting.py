from typing import List, Tuple
import os
from pathlib import Path
import argparse
import random


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
    A_path = path / A
    B_path = path / B
    a_files = sorted([p for p in A_path.glob("*.png")])
    b_files = sorted([p for p in B_path.glob("*.png")])
    return a_files, b_files


def check_existence(
        filenames: List[Path]) -> None:
    """
    Check if the paths exist.
    Args:
        filenames (List[Path]): List of filenames.
    Returns:
        None
    """
    for f in filenames:
        if not f.exists():
            raise FileNotFoundError(f"Missing file: {f}")

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
    for folder in folder_list:
        full_path = input_dir / folder
        full_path.mkdir(parents=True, exist_ok=True)


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
    total = filenames.copy()
    random.shuffle(total)
    train_size = int(len(total) * alpha)
    return total[:train_size], total[train_size:]


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
    for f in filenames:
        dest = split_dir / f.name
        if not dest.exists():
            os.symlink(f.resolve(), dest)


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
    input_path = Path(input_dir)
    a_files, b_files = browse_folder(input_path, A, B)

    check_existence(a_files + b_files)
    create_folders(input_path, folders)

    a_train, a_test = split_train_test(a_files, alpha)
    b_train, b_test = split_train_test(b_files, alpha)

    create_symlinks(a_train, input_path / A, input_path / folders[0])  # trainA
    create_symlinks(b_train, input_path / B, input_path / folders[1])  # trainB
    create_symlinks(a_test, input_path / A, input_path / folders[2])   # testA
    create_symlinks(b_test, input_path / B, input_path / folders[3])   # testB



def main():
    """
    Main function to execute the script.
    """
    parser = build_argparser()
    args = parser.parse_args()

    process(args.input_dir, args.A, args.B, args.folders, args.alpha)


if __name__ == "__main__":
    main()



