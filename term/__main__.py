import logging
import traceback
from typing import List

from term import ERROR_FOLDER_DIR, LOSE_FOLDER_DIR, WIN_FOLDER_DIR
from term.filter import Filter
from term.page.elements import Term
from term.utils import (create_result_folders, get_driver,
                        move_and_rename_log_files)


class Win(Exception):
    ...


class Lose(Exception):
    ...


class Crawler:
    def __init__(self, page_elements: Term) -> None:
        self.page = page_elements

    def send_letters_in_cells(self, cells: list, word: List) -> None:
        [cell.send_keys(letter) for cell, letter in zip(cells, word)]

    def check_win(self, attributes: List[str]) -> None:
        for attribute in attributes:
            if 'correta' not in attribute:
                return
        raise (Win)

    def run(self):
        rows = self.page.get_rows_with_cells()
        filter = Filter()
        for row in rows:
            word = filter.get_random_word()
            self.send_letters_in_cells(row.cells, list(word))
            self.page.confirm_word()
            attributes = self.page.get_webelements_attribute(row.cells)
            self.check_win(attributes)
            filter.filter_words_list(attributes)
        raise (Lose)


if __name__ == '__main__':
    try:
        create_result_folders()
        driver = get_driver()
        crawler = Crawler(Term(driver))
        crawler.run()
        driver.quit()
    except Win:
        print('Win!')
        move_and_rename_log_files(WIN_FOLDER_DIR)
    except Lose:
        print('Lose!')
        move_and_rename_log_files(LOSE_FOLDER_DIR)
    except Exception:
        logging.info(traceback.format_exc())
        move_and_rename_log_files(ERROR_FOLDER_DIR)
    finally:
        driver.quit()
