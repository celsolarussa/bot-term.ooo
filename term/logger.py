import logging
from pathlib import Path

from term import utils

HANDLERS = []


def my_logger(logger_name, logger_path, crawler_number):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(str(logger_path))
    formatter = logging.Formatter(
        f'%(asctime)s:Thread({crawler_number}):%(message)s'
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    HANDLERS.append(logger.handlers)
    return logger


def configure_logger(crawler_number, folder_path):
    logger_name = utils.get_formatted_datetime(
        prefix=f'{crawler_number}-', suffix='.log'
    )
    logger_path = folder_path / Path(logger_name)
    return logger_name, logger_path


def get_loggers(folder_path, crawler_number):
    log_name, log_path = configure_logger(crawler_number, folder_path)
    logger = my_logger(log_name, log_path, crawler_number)
    return logger


def clear_handlers():
    [i.clear() for i in HANDLERS]
