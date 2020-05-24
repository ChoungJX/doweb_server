import datetime


def get_now() -> str:
    now_time = datetime.datetime.now()
    return datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
