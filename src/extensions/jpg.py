import os
import shutil
from collections import defaultdict
from datetime import datetime
from time import sleep

from exif import Image as ExifImage
from PIL import Image
from tqdm import tqdm

from src.metadata.country import find_closest_country, get_country_from_gps
from src.utils.config import logger
from src.utils.utils import (
    clean_str,
    get_datetime,
    get_gps_from_exif,
    is_unique_and_get_id,
)


def move_jpeg_to_jpg(src_folder, dest_folder):
    for root, _, files in os.walk(src_folder):
        for file in files:
            # Create the new file name with '.jpg' extension
            file_jpg = os.path.splitext(file)[0] + ".jpg"

            # Create full paths for source and destination files
            jpeg_file_path = os.path.join(root, file)
            jpg_file_path = os.path.join(dest_folder, file_jpg)

            # Ensure the destination folder exists
            os.makedirs(dest_folder, exist_ok=True)

            # Open the JPEG file and save it as a JPG file in the destination folder
            with Image.open(jpeg_file_path) as img:
                # Extract EXIF data
                exif_data = img.info.get("exif")
                if not exif_data:
                    exif_data = {}

                # Save it as a JPG file with the same EXIF data
                img.save(jpg_file_path, "JPEG", exif=exif_data)

            # Delete the original JPEG file
            os.remove(jpeg_file_path)


def set_up_jpg_grouped_by_date(src_folder):
    jpg_grouped_by_date = defaultdict(list)

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as image_file:
                my_image = ExifImage(image_file)

                all_exifs_tags = my_image.list_all()
                if "datetime_original" in all_exifs_tags:
                    date_time = my_image.datetime_original
                elif "datetime" in all_exifs_tags:
                    date_time = my_image.datetime
                else:
                    # Use file's last modification time
                    last_modified_timestamp = os.path.getmtime(file_path)
                    last_modified_date_time = datetime.fromtimestamp(
                        last_modified_timestamp
                    )
                    formatted_date_time = last_modified_date_time.strftime(
                        "%Y:%m:%d %H:%M:%S"
                    )

                    # Set new datetime tag
                    my_image.datetime = formatted_date_time
                    date_time = formatted_date_time

                    # Write the image with modified EXIF data back to file
                    with open(file_path, "wb") as new_image_file:
                        new_image_file.write(my_image.get_file())

                year, month, day, _, _ = get_datetime(date_time)
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
            exif_image = ExifImage(file_path)
            all_exifs_tags = exif_image.list_all()
            if "datetime" in all_exifs_tags:
                date_time = exif_image.datetime
            if "datetime_original" in all_exifs_tags:
                date_time = exif_image.datetime_original

            year, month, day, hour, minute = get_datetime(date_time)
            datetime_obj = datetime(
                int(year), int(month), int(day), int(hour), int(minute)
            )
            if "model" not in all_exifs_tags:
                exif_image.model = "unknown"
            device = clean_str(exif_image.model)

            if [
                "gps_latitude",
                "gps_latitude_ref",
                "gps_longitude",
                "gps_longitude_ref",
            ] not in all_exifs_tags:
                country = "unknown"
            else:
                latitude, longitude = get_gps_from_exif(
                    exif_image.gps_latitude,
                    exif_image.gps_latitude_ref,
                    exif_image.gps_longitude,
                    exif_image.gps_longitude_ref,
                )
                country = get_country_from_gps(latitude, longitude)
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
