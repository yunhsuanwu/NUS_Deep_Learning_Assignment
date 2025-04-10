import os
import requests
from datetime import datetime, timedelta
import argparse


def build_argparser() -> argparse.ArgumentParser:
    """
    Build the argument parser for command line arguments.
    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description="Process real clouds dataset.")
    parser.add_argument(
        "--start_date", type=str, required=True,
        help="Start date for downloading images (format: YYYY-MM-DD)."
    )
    parser.add_argument(
        "--end_date", type=str, required=True,
        help="End date for downloading images (format: YYYY-MM-DD)."
    )
    parser.add_argument(
        "--output_dir", type=str, required=True,
        help="Directory to save the images."
    )
    return parser


def download_images(
        start_date: str, 
        end_date: str, 
        output_dir: str) -> None:
    """
    Downloads satellite images from NEA from start_date to end_date (inclusive).
    
    Args:
        start_date (str): Format 'YYYY-MM-DD'
        end_date (str): Format 'YYYY-MM-DD'
        output_dir (str): Directory to save images
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
    download_images(args.start_date, args.end_date, args.output_dir)


if __name__ == "__main__":
   main()
    