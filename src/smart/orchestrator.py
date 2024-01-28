import os
import shutil

from src.extensions.jpg import handle_jpg
from src.utils.config import ALLOWED_EXTENSIONS, logger
from src.utils.utils import get_file_extension


class MediaOrchestrator:
    def __init__(
        self, bronze_storage: str, silver_storage: str, gold_storage: str
    ) -> None:
        self.bronze_storage = bronze_storage
        self.silver_storage = silver_storage
        self.gold_storage = gold_storage
        self.silver_storage_folders = []

    def bronze_to_silver(self):
        for root, _, files in os.walk(self.bronze_storage):
            for file in files:
                extension = get_file_extension(file_name=file)
                if extension in ALLOWED_EXTENSIONS:
                    extension_folder = os.path.join(self.silver_storage, extension)
                    os.makedirs(extension_folder, exist_ok=True)
                    if extension_folder not in self.silver_storage_folders:
                        self.silver_storage_folders.append(extension_folder)
                    shutil.move(
                        os.path.join(root, file), os.path.join(extension_folder, file)
                    )
                else:
                    logger.error(f"Skipping unrecognized extension {file}")

    def silver_to_gold(self):
        for folder in self.silver_storage_folders:
            extension = folder.split("\\")[-1]
            match extension:
                case "jpg":
                    handle_jpg(src_folder=folder, dest_folder=self.gold_storage)
                case "jpeg":
                    logger.info(f"Not Implemented {extension}")
                case "png":
                    logger.info(f"Not Implemented {extension}")
                case "mp4":
                    logger.info(f"Not Implemented {extension}")
                case "mov":
                    logger.info(f"Not Implemented {extension}")
                case _:
                    logger.error(f"Skipping unrecognized extension {extension}")
