from typing import Optional, Tuple

from PIL import Image
from PIL.ExifTags import TAGS

from src.utils.utils import get_decimal_from_dms


def get_exif_data(image_path):
    with Image.open(image_path) as img:
        exif_raw = img._getexif()
        if not exif_raw:
            return None
        exif = {TAGS[k]: v for k, v in exif_raw.items() if k in TAGS}
    return exif


def get_datetime_from_exif(exif) -> Optional[Tuple]:
    try:
        # Extracting the date
        date_time = exif.get("DateTimeOriginal") or exif.get("DateTime")
        date, time = date_time.split(" ")
        year, month, day = date.split(":")[:3]
        hour, minute = time.split(":")[:2]
        return year, month, day, hour, minute
    except KeyError:
        return None
    except AttributeError:
        return None


def get_gps_from_exif(exif) -> tuple[float, float]:
    if "GPSInfo" in exif:
        gps_info = exif["GPSInfo"]
        gps_latitude = gps_info.get(2)
        gps_latitude_ref = gps_info.get(1)
        gps_longitude = gps_info.get(4)
        gps_longitude_ref = gps_info.get(3)

        if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
            latitude = get_decimal_from_dms(gps_latitude, gps_latitude_ref)
            longitude = get_decimal_from_dms(gps_longitude, gps_longitude_ref)
            return latitude, longitude
    return None, None
