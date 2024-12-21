from datetime import datetime

_default_hour_notify_ = 15

_monthes = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

_monthesNum = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


def get_num_month_by_string(month: str) -> int:
    return _monthes.get(month, 1)


def get_month_days(year: int, month: int) -> int:
    _next_month = month + 1
    _next_month_year = year
    if _next_month > 12:
        _next_month_year += 1
        _next_month = 1
    _start_month = datetime(year, month, 1, 0, 0, 0)
    _start_next_month = datetime(_next_month_year, _next_month, 1, 0, 0, 0)

    _days = int((_start_next_month.timestamp() - _start_month.timestamp()) / 86400)

    return _days
