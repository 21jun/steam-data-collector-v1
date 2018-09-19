from datetime import datetime


def get_full_date():
    # return string type yyyy-mm-dd hh:mm:ss
    now = datetime.now()
    result = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return result
