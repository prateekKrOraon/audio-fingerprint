import arrow
import os
import mimetypes


def date_time_format(date_str):
    """Constructs easy human readable date format from.

    Returns:
        str: Date.
    """

    dt = arrow.get(date_str)
    return dt.humanize()


def file_type(key):
    """Gets file extension.

    Returns:
        str: File extension.
    """
    
    file_info = os.path.splitext(key)
    file_extension = file_info[1]

    try:
        return mimetypes.types_map[file_extension.lower()]
    except Exception as e:
        return 'unknown'
