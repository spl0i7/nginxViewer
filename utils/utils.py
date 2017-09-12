import datetime


async def get_aggregration_count(x, field):
    results = []
    async for doc in x:
        results.append(doc)
    try:
        return results[0][field]
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
