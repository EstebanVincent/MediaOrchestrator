import datetime
import os
import shutil
from collections import defaultdict
from time import sleep

from PIL import Image
from tqdm import tqdm

from src.metadata.country import find_closest_country, get_country_from_gps
from src.metadata.exif import get_datetime_from_exif, get_exif_data, get_gps_from_exif
from src.utils.config import logger
from src.utils.utils import clean_str, is_unique_and_get_id


def convert_jpeg_to_jpg(root, file_jpeg):
    # Create the new file path with '.jpg' extension
    file_jpg = os.path.splitext(file_jpeg)[0] + ".jpg"
    jpeg_file_path = os.path.join(root, file_jpeg)
    jpg_file_path = os.path.join(root, file_jpg)

    # Open the JPEG file and save it as a JPG file
    with Image.open(jpeg_file_path) as img:
        # Extract EXIF data
        exif_data = img.info.get("exif")

        # Save it as a JPG file with the same EXIF data
        img.save(jpg_file_path, "JPEG", exif=exif_data)

    return jpg_file_path


def set_up_jpg_grouped_by_date(src_folder):
    jpg_grouped_by_date = defaultdict(list)
    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            exif = get_exif_data(file_path)
            if not exif:
                logger.info(f"Skipping No Exif {file_path}")
                continue
            date_time = get_datetime_from_exif(exif)
            if not date_time:
                logger.info(f"Skipping No Date Time {file_path}")
                continue
            year, month, day, _, _ = date_time
            jpg_grouped_by_date[(year, month, day)].append(file_path)
    return jpg_grouped_by_date


def handle_jpg(src_folder, dest_folder):
    jpg_grouped_by_date = set_up_jpg_grouped_by_date(src_folder)

    # Moving files
    for date, file_paths in tqdm(
        jpg_grouped_by_date.items(), desc="Processing batches", unit="Day"
    ):
        day_batch = {}
        # Setting up the batch
        for file_path in tqdm(file_paths, desc=f"\nSet Up {date}", unit="file"):
            exif = get_exif_data(file_path)

            date_time = get_datetime_from_exif(exif)

            year, month, day, hour, minute = date_time
            datetime_obj = datetime.datetime(
                int(year), int(month), int(day), int(hour), int(minute)
            )
            device = clean_str(exif.get("Model", "Unknown"))
            latitude, longitude = get_gps_from_exif(exif)
            if latitude and longitude:
                country = get_country_from_gps(latitude, longitude)
            else:
                country = "unknown"
            day_batch[file_path] = {
                "time": datetime_obj,
                "country": country,
                "device": device,
            }

        for file_path, info in tqdm(
            day_batch.items(), desc=f"Country Fix {date}", unit="file"
        ):
            if info["country"] == "Unknown":
                info["country"] = find_closest_country(
                    day_batch, info["time"], info["device"]
                )
        sleep(0.1)
        for file_path, info in tqdm(
            day_batch.items(), desc=f"Move {date}", unit="file"
        ):
            new_folder = os.path.join(
                dest_folder,
                str(info["time"].year),
                str(info["time"].month),
                info["device"],
                info["country"],
            )

            datetime_pattern = f"{year}{month}{day}_{hour}{minute}"

            result = is_unique_and_get_id(new_folder, file_path, datetime_pattern)
            if not result["unique"]:
                logger.warning(f"Skipping duplicate {file_path}")
                continue
            os.makedirs(new_folder, exist_ok=True)
            extension = file_path.lower().split(".")[-1]
            new_file_name = f"{info['time'].strftime('%Y%m%d_%H%M')}_{str(result['id']).zfill(3)}.{extension}"
            shutil.move(file_path, os.path.join(new_folder, new_file_name))
