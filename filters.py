import arrow
import os
import mimetypes


def date_time_format(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()


def file_type(key):
    file_info = os.path.splitext(key)
    file_extension = file_info[1]

    try:
        return mimetypes.types_map[file_extension.lower()]
    except Exception as e:
        return 'unknown'
