from pathlib import Path
from typing import List

from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options


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
