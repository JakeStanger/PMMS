import re


def get_name_sort(name: str):
    if not name:
        return None
    return re.match('(?:The |A )?(.*)', name)[1]
