import geopandas as gpd
from PIL import Image

from src.utils.logger import setup_logger

Image.MAX_IMAGE_PIXELS = None

gdf = gpd.read_file("TM_WORLD_BORDERS_SIMPL-0.3/TM_WORLD_BORDERS_SIMPL-0.3.shp")

logger = setup_logger("activity.log")

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "mp4", "mov"]
