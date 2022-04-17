import uuid
from datetime import datetime
from functools import wraps
from time import sleep
import logging

from dateutil import parser


def ISO_parse(created: str, modified: str) -> (datetime, datetime):
    return parser.parse(created), parser.parse(modified)


def multiple_uuid_parse(*args: str):
    return (uuid.UUID(i) for i in args)


def cast_types(data_id, created, modified):
    if not isinstance(data_id, uuid.UUID):
        data_id = uuid.UUID(data_id)

    if all([not isinstance(created, datetime), not isinstance(modified, datetime)]):
        created, modified = ISO_parse(created, modified)

    return data_id, created, modified


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except BaseException as e:
                    seconds = start_sleep_time * factor ** n
                    if seconds < border_sleep_time:
                        n += 1
                    else:
                        seconds = border_sleep_time
                    logging.error(f'{e}\nRetry after {seconds} seconds')
                    sleep(seconds)

        return inner

    return func_wrapper
