import datetime


def get_aggregration_count(x, field):
    try:
        return list(x)[0][field]
    except:
        return 0


def get_since_today(timespan):
    since = datetime.datetime.min
    today = datetime.datetime.today()

    if timespan == 'day':
        since = today - datetime.timedelta(days=1)
    elif timespan == 'week':
        since = today - datetime.timedelta(days=7)
    elif timespan == 'month':
        since = today - datetime.timedelta(days=30)
    return since
