from datetime import datetime


def date_pass():
    now = datetime.now()
    result = "%s-%s-%s %s:%s:%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return result
