from datetime import datetime, date
from dateutil.parser import parse as date_parse


def readable_when(date_: datetime | date | str) -> str:
    if isinstance(date_, date):
        date_ = datetime.combine(date_, datetime.min.time())

    try:
        date_ = date_parse(date_)  # type: ignore
    except ValueError:
        raise ValueError(
            "Invalid date. Must be a datetime, date, or datetime/date string."
        )

    minutes_ago = (datetime.now() - date_).total_seconds() / 60
    if minutes_ago < 1:
        return "Just now"
    if minutes_ago < 60:
        return f"{int(minutes_ago)} minutes ago"
    hours_ago = minutes_ago / 60
    if hours_ago < 24:
        return f"{int(hours_ago)} hours ago"
    return date_.strftime("%B %d, %Y")
