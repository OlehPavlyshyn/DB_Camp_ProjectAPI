import datetime

def get_date_key():
    now = datetime.datetime.now()
    year = str(now.year)
    if now.month < 10:
        month = str("0%i" % now.month)
    else:
        month = str(now.month)
    if now.day < 10:
        day = str("0%i" % now.day)
    else:
        day = str(now.day)

    if now.hour < 10:
        hour = str("0%i" % now.hour)
    else:
        hour = str(now.hour)
    if now.minute < 10:
        minute = str("0%i" % now.minute)
    else:
        minute = str(now.minute)
    date = int("%s%s%s%s%s" % (year[2:],month,day,hour,minute))
    return date
