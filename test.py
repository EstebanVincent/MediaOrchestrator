import os
from datetime import datetime

last_modified_timestamp = os.path.getmtime(
    "D:\\Users\\estev\\Pictures\\dev\\silver\\jpg\\FB_IMG_1666054906081.jpg"
)
date_time = datetime.fromtimestamp(last_modified_timestamp)
formatted_date_time = date_time.strftime("%Y:%m:%d %H:%M:%S")
print(formatted_date_time)
