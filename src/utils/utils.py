import glob
import hashlib
import os


def get_file_extension(file_name: str) -> str:
    return file_name.lower().split(".")[-1]


def clean_str(string: str) -> str:
    # Remove non-printable characters and strip trailing whitespace/null characters
    return "".join(char for char in string if char.isprintable()).rstrip()


def hash_file(file_path: str):
    """Generate a hash for a file."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def is_unique_and_get_id(dest_dir, to_be_added, datetime_pattern):
    # Generate the pattern to match files
    file_pattern = os.path.join(dest_dir, f"{datetime_pattern}_*.*")
    matches = glob.glob(file_pattern)
    # Find files in the destination directory matching the datetime pattern
    for file_path in matches:
        # Calculate the hash of each file and compare
        if hash_file(file_path) == hash_file(to_be_added):
            return {"unique": False}
    return {"unique": True, "id": len(matches) + 1}


def get_decimal_from_dms(dms, ref) -> float:
    degrees, minutes, seconds = dms
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ["S", "W"]:
        decimal = -decimal
    return float(decimal)
