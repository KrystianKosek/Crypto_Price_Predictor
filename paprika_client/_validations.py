import datetime
from _exceptions import *


def is_date_valid(date: str) -> bool:
    """
    Parameters:
        date: str - date string-like, formatted "YYYY-MM-DD"
    Returns:
        bool - returns True if date parameter is valid date in format YYYY-MM-DD, otherwise False
    """
    valid = True
    yy, mm, dd = date.split('-')

    try:
        datetime.datetime(int(yy), int(dd), int(mm))
    except ValueError as e:
        valid = False

    return valid


def code_error(status_code: int) -> None:
    """
    Parameters:
        status_code: int - status code of request
    Retruns:
        If status_code parameter is above or equal to 400 (status_code is HTTP error code) raises custom made
        exception - RequestCodeError
    """
    if status_code >= 400:
        raise RequestCodeError("Error while fetching data", status_code)