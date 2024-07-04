# src/get_time.py


def get_time():
    """Gets the current time formatted as a string.

    Returns:
        str: The current time formatted as 'YYYYMMDDTHHMMSS'.
    """
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%dT%H%M%S")
    return formatted_now
