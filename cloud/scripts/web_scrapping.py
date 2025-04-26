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
    import os
    import requests
    from datetime import datetime, timedelta

    base_url = "https://www.nea.gov.sg/docs/default-source/satelliteimage/BlueMarbleASEAN_"
    dt = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_time = dt
    while current_time <= end:
        for hour in range(0, 24):
            for minute in [0, 20, 40]:
                timestamp = current_time.strftime("%Y%m%d") + f"_{hour:02d}{minute:02d}"
                image_url = f"{base_url}{timestamp}.jpg"
                save_path = os.path.join(output_dir, f"{timestamp}.jpg")

                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(save_path, "wb") as f:
                            f.write(response.content)
                        print(f"✅ Downloaded {timestamp}")
                    else:
                        print(f"❌ Not found: {timestamp}")
                except Exception as e:
                    print(f"⚠️ Error downloading {timestamp}: {e}")
        current_time += timedelta(days=1)
        
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
    