import datetime


def is_same_month(a, b):
    return a.year != b.year or a.month != b.month


def sort_dates(dates_list):
    '''
    Outputs list of dicts, each representing one month and its tours.
    '''
    dates = []
    current_month = {}
    last_date = datetime.date(1, 1, 1)
    for date in dates_list:
        is_not_current_month = last_date.year != date.start_date.year or last_date.month != date.start_date.month
        if is_not_current_month:
            dates.append({'month': date.start_date, 'dates': []})
            current_month = dates[-1]
            last_date = date.start_date
        current_month['dates'].append(date)
    return dates
    # if len(dates_list) == 0:
    #     return []
    # dates = []
    # current_month = {'month': dates_list[0].start_date, 'dates': []}
    # delta_month = datetime.timedelta()
    # for date in dates_list:
    #     while not is_same_month(current_month['month'], date.start_date):
    #         current_month = {'month': }


def count(iterable):
    return sum(1 for _ in iterable)
