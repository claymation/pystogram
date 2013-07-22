import calendar


# FIXME: i18n/l10n? strptime parsing should alleviate this concern.
MONTHS = dict({ (v,k) for k,v in enumerate(calendar.month_abbr) })
