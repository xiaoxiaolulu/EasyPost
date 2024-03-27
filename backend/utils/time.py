import calendar
import datetime
from typing import List


def now_time():
    """
    获取当前时间。

    :return: 返回当前时间的datetime对象。
    :rtype: datetime.datetime
    """
    return datetime.datetime.now()


def current_date():
    """
    获取当前日期。

    :return: 返回当前日期的date对象。
    :rtype: datetime.date
    """
    return now_time().date()


def day_num():
    """
    获取当前星期几（数字形式）。

    :return: 返回当前星期几的数字表示形式，其中周一为1，周日为7。
    :rtype: int
    """
    return now_time().isoweekday()


def week_start():
    """
    获取当前星期的开始日期。

    :return: 返回当前星期的开始日期的date对象。
    :rtype: datetime.date
    """
    return (now_time() - datetime.timedelta(days=day_num()) + datetime.timedelta(days=1)).date()


def week_end():
    """
    获取当前星期的结束日期。

    :return: 返回当前星期的结束日期的date对象。
    :rtype: datetime.date
    """
    return (now_time() - datetime.timedelta(days=day_num()) + datetime.timedelta(days=7)).date()


def month_start():
    """
    获取当前月份的开始日期。

    :return: 返回当前月份的开始日期的datetime对象。
    :rtype: datetime.datetime
    """
    return datetime.datetime(now_time().year, now_time().month, 1)


def month_end():
    """
    获取当前月份的结束日期。

    :return: 返回当前月份的结束日期的datetime对象。
    :rtype: datetime.datetime
    """
    now = now_time()
    return datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]) + datetime.timedelta(
        hours=23, minutes=59, seconds=59)


def yesterday():
    """
    获取昨天的日期和时间。

    :return: 返回昨天的日期和时间，格式为'YYYY-MM-DD HH:MM:SS'。
    :rtype: str
    """
    return (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d-%H:%M:%S')


def get_before_day(days: int) -> List[datetime.date]:
    """
    获取指定天数前的日期列表。

    参数:
    days (int): 需要获取的天数。

    返回:
    List[date]: 指定天数前的日期列表。
    """
    today = datetime.date.today()
    date_list = [today - datetime.timedelta(days=i) for i in range(days)]
    return date_list
