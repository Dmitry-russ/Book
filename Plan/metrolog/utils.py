import calendar
import datetime


def add_months(sourcedate, months):
    """Функция расчета даты окончания поверки."""

    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
