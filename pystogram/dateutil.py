import calendar
import datetime


# FIXME: i18n/l10n?
MONTHS = dict({ (v,k) for k,v in enumerate(calendar.month_abbr) })

YEAR = 60 * 60 * 24 * 365
MONTH = 60 * 60 * 24 * 30
DAY = 60 * 60 * 24
HOUR = 60 * 60
MINUTE = 60
SECOND = 1


def timedelta_from_seconds(total_seconds):
    return datetime.timedelta(days=total_seconds / 86400, seconds=total_seconds % 86400)


def guess_resolution(seconds):
    if seconds > YEAR:
        return YEAR
    elif seconds > MONTH:
        return MONTH
    elif seconds > DAY:
        return DAY
    elif seconds > HOUR:
        return HOUR
    elif seconds > MINUTE:
        return MINUTE
    else:
        return SECOND
