from datetime import datetime

from shapely.geometry import Point

from src.utils.config import gdf


def get_country_from_gps(latitude, longitude) -> str:
    point = Point(longitude, latitude)
    for _, row in gdf.iterrows():
        if row["geometry"].contains(point):
            return row["NAME"]
    return "Unknown"


def find_closest_country(image_dict: dict, target_time: datetime, device: str) -> str:
    # Sort images by time difference from the target
    sorted_images = sorted(
        image_dict.items(), key=lambda item: abs(item[1]["time"] - target_time)
    )
    # Find the closest image with known country from the same device
    for _, image_info in sorted_images:
        if image_info["country"] != "Unknown" and image_info["device"] == device:
            return image_info["country"]
    return "Unknown"
