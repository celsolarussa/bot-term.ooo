from pathlib import Path
from typing import List

from term.page.elements import Term
from term.utils import get_driver, get_words_list

PROJECT_DIR = Path('.').parent.resolve()
words_file_path = PROJECT_DIR / 'words.txt'


class Crawler:
    def __init__(self, words_list: List[str], page_elements: Term) -> None:
        self.words_list = words_list
        self.page = page_elements

    def run(self):
        ...


if __name__ == '__main__':
    driver = get_driver()
    words_list = get_words_list(words_file_path)
    page = Term(driver)
