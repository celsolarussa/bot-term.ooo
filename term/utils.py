import logging
from datetime import datetime
from pathlib import Path
from typing import List

from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options

from term import (ERROR_FOLDER_DIR, LOG_FILE_DIR, LOSE_FOLDER_DIR,
                  RESULT_FOLDER_DIR, WIN_FOLDER_DIR)

logging.basicConfig(
    format='%(asctime)s::%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
    filename='logs.log',
    filemode='w',
    level=logging.INFO,
)


def get_words_list(file_path: Path) -> List[str]:
    with open(file_path, 'r') as f:
        words = f.read()
        return words.split(' ')


def get_driver():
    options = Options()
    options.add_argument('--start-maximized')
    driver = Remote(
        command_executor='http://127.0.0.1:4444/wd/hub', options=options
    )
    return driver


def create_result_folders():
    RESULT_FOLDER_DIR.mkdir(exist_ok=True)
    ERROR_FOLDER_DIR.mkdir(exist_ok=True)
    LOSE_FOLDER_DIR.mkdir(exist_ok=True)
    WIN_FOLDER_DIR.mkdir(exist_ok=True)


def move_and_rename_log_files(destinaton_path: Path):
    logging.shutdown()
    log_name = datetime.now().strftime('%d%m%Y%H%S%M') + '.log'
    new_log_path = destinaton_path / log_name
    LOG_FILE_DIR.rename(new_log_path)
