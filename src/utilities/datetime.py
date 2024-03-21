import pytz
from dateutil import parser


def convert_to_different_tz(time_str, from_tz_str, to_tz_str, format_str="%d %b %Y %I:%M:%S %p"):
    # Parse the given time string
    dt = parser.parse(time_str)

    # Get the timezone objects for the given timezones
    from_tz = pytz.timezone(from_tz_str)
    to_tz = pytz.timezone(to_tz_str)

    # Localize the datetime object to the source timezone
    dt_from = from_tz.localize(dt)

    # Convert the localized datetime to the target timezone
    dt_to = dt_from.astimezone(to_tz)

    # Format the datetime object as per the specified format
    converted_time = dt_to.strftime(format_str)

    return converted_time
