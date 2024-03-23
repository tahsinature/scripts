from typing import Literal, Union
import pytz
from dateutil import parser
from datetime import datetime, timedelta


def try_to_parse_date_or_time(date_or_time: str):
    try:
        return parser.parse(date_or_time)
    except ValueError:
        return None


def convert_to_different_tz(dt: datetime, to_tz_str: str):
    to_tz = pytz.timezone(to_tz_str)
    return dt.astimezone(to_tz)


"""
    - {{"title":"title","when":{"time":"10:00 pm","timezone":"America/Los_Angeles","date":"20 Sep 2023","date_type":"absolute"}}}
    - {{"title":"title","when":{"time":"10:00 pm","timezone":"America/Los_Angeles","date":1,"date_type":"relative"}}} // 0 means no date / today. 1 means tomorrow. -1 means yesterday and so on.
"""
# calculate_time function will return the time in the given timezone and date.


def calculate_time(time: str, timezone: str, date: Union[str, int], date_type: Literal["absolute", "relative"]):
    # Convert time to datetime object
    # time_format = "%I:%M %p"  # Example format: "10:00 pm"
    # datetime_obj = datetime.strptime(time, time_format)

    datetime_obj = try_to_parse_date_or_time(time)
    if datetime_obj is None:
        raise ValueError("Invalid time format. Please provide the time in the format '10:00 pm'.")

    # If date_type is "absolute", use the provided date
    if date_type == "absolute":
        if isinstance(date, int):
            raise ValueError("For 'absolute' date_type, date should be a string representing the date.")
        date_obj = datetime.strptime(date, "%d %b %Y")
    # If date_type is "relative", calculate the date based on the provided integer
    elif date_type == "relative":
        if not isinstance(date, int):
            raise ValueError("For 'relative' date_type, date should be an integer representing the offset.")
        today = datetime.now(pytz.timezone(timezone)).date()
        date_obj = today + timedelta(days=date)
    else:
        raise ValueError("Invalid date_type. It should be either 'absolute' or 'relative'.")

    # Combine date and time
    combined_datetime = datetime.combine(date_obj, datetime_obj.time())

    # Convert to the specified timezone
    tz = pytz.timezone(timezone)
    combined_datetime = tz.localize(combined_datetime)

    return combined_datetime
