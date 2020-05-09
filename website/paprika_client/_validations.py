import datetime
from ._exceptions import RequestCodeError


def is_date_valid(date: str) -> bool:
    valid = True
    yy, mm, dd = date.split('-')
    try:
        datetime.datetime(int(yy), int(mm), int(dd))
    except ValueError as e:
        print(e)
        valid = False

    return valid


def code_error(status_code: int) -> None:
    if status_code >= 400:
        raise RequestCodeError("Error while fetching data", status_code)