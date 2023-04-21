"""
Contains a bunch of functions to help with handling time.
"""

import datetime
from datetime import timezone  # Woks with >= Python 3.2.  See https://tinyurl.com/yywwmgpg

EPOCH = datetime.datetime(1970, 1, 1)
SECONDS_IN_A_DAY = 24 * 60 * 60  # 86400


def epoch():
    """
   Returns a datetime object that represents the beginning of time (1970-01-01 00:00:00, GMT)
   """
    return EPOCH


def seconds_in_day():
    """
   Returns the number of seconds in a day   :return:
   """
    return SECONDS_IN_A_DAY


def right_now():
    """
   Returns a datetime object representing right now (the time at which this function was called), in UTC of course.   No need to fuss with timezones   :return:
   """
    # We are interested in utcnow(), not now(), which reflects the local tz
    # return datetime.datetime.utcnow()

    return datetime.datetime.now(timezone.utc)


def today():
    """
   Returns today (in UTC).   :return:
   """
    return right_now().replace(hour=0, minute=0, second=0, microsecond=0)


def today_almost_midnight():
    """
   Returns today at 23:59:59 (in UTC)   :return:
   """
    return today().replace(hour=23, minute=59, second=59)


def yesterday():
    """
   Returns yesterday in UTC   :return:
   """
    return today() - datetime.timedelta(1)


def yesterday_almost_midnight():
    """
   Returns yesterday at 23:59:59 (in UTC)   :return:
   """
    return yesterday().replace(hour=23, minute=59, second=59)


def tomorrow():
    """
   Returns tomorrow in UTC   :return:
   """
    return today() + datetime.timedelta(1)


def tomorrow_almost_midnight():
    """
   Returns tomorrow at 23:59:59 (in UTC)   :return:
   """
    return tomorrow().replace(hour=23, minute=59, second=59)


def date_add(some_datetime, days_to_add):
    """
   Adds a number of days to a date_time object   :param some_datetime: Some date time object   :param days_to_add: Some number of days to add (int)   :return:
   """
    # Validate some_datetime
    if type(some_datetime) is not datetime.datetime:
        raise ValueError(f"{str(some_datetime)} is not a datetime.  It is a {type(some_datetime)}.")

        # Validate days to add
    if type(days_to_add) is not int:
        raise ValueError(f"{str(days_to_add)} is not an integer.  It is a {type(days_to_add)}.")

    return some_datetime + datetime.timedelta(days_to_add)


def date_sub(some_datetime, days_to_subtract):
    """
   Subtracts a number of days to a date_Time objects   :param some_datetime: Some date time object   :param days_to_subtract: Some number of days to subtract (int)   :return:
   """
    return date_add(some_datetime=some_datetime, days_to_add=(days_to_subtract * -1))


def date_as_string(some_datetime, date_format='%Y-%m-%d'):
    """
   Returns a date with a given format, defaulting to YYYY-MM-DD   :param some_datetime: a datetime object   :param date_format: The date format we care to format as   :return:
   """
    return datetime.datetime.strftime(some_datetime, date_format)


def date_as_timestamp(some_datetime, as_ms=False):
    """
   Returns the date as a timestamp representing the number of seconds that have passed since the epoch   :type as_ms: if Set to True will return the timestamp as milliseconds rather than just seconds   :param some_datetime:
   :return:
   """
    ret_val = int(datetime.datetime.timestamp(some_datetime))

    if as_ms is True:
        ret_val = ret_val * 1000

    return ret_val


if __name__ == '__main__':
    print(f"epoch = {epoch()}, which is of type {type(epoch())}")
    print(f"seconds_in_day = {seconds_in_day()}, which is of type {type(seconds_in_day())}")
    print(f"right_now = {right_now()}, which is of type {type(right_now())}")
    print(f"today = {today()}, which is of type {type(today())}")
    print(f"today_almost_midnight = {today_almost_midnight()}, which is of type {type(today_almost_midnight())}")
    print(f"yesterday = {yesterday()}, which is of type {type(yesterday())}")
    print(f"tomorrow = {tomorrow()}, which is of type {type(tomorrow())}")

    tam = tomorrow_almost_midnight()
    print(f"tomorrow almost midnight is {tam}")
    print(f"day after tomorrow almost midnight is {date_add(tam, 1)}")
    print(f"yesterday almost midnight is {date_sub(tam, 1)}")

    print(f"Today as timestamp = {date_as_timestamp(today())}")
    print(f"Right now as timestamp = {date_as_timestamp(right_now())}")
