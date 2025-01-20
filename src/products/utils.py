import math

def get_page_data(curr, page_size, count):
    """Function to get pagination details."""
    last = math.ceil(count / page_size)
    start = 1 if count > 0 else None
    return {
        "start": start,
        "previous": curr - 1 if curr > 1 else None,
        "current": curr,
        "next": curr + 1 if curr < last else None,
        "last": last,
        "count": count,
    }