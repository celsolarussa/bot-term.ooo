from typing import List

from term.filter import Filter
from term.page.elements import Term
from term.utils import get_driver
from term.filter import PATTERN_CORRECT


class Win(Exception):
    ...


class Lose(Exception):
    ...


class Crawler:
    def __init__(self, page_elements: Term) -> None:
        self.page = page_elements

    def send_letters_in_cells(self, cells: list, word: List) -> None:
        [cell.send_keys(letter) for cell, letter in zip(cells, word)]

    def check_win(self):
        if '\\w' not in PATTERN_CORRECT:
            raise(Win)

    def run(self):
        rows = self.page.get_table_rows()
        filter = Filter()
        for row in rows:
            word = filter.get_random_word()
            self.send_letters_in_cells(row.cells, word)
            self.page.confirm_word()
            attributes = self.page.get_webelements_attribute(row.cells)
            filter.filter_words_list(attributes)
            self.check_win()
        raise(Lose)


if __name__ == '__main__':
    driver = get_driver()
    crawler = Crawler(Term(driver))
    crawler.run()
