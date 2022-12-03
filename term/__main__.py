# import os
import traceback
from bdb import BdbQuit
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from term import (ERROR_FOLDER_DIR, LOGS_FOLDER_DIR, LOSE_FOLDER_DIR,
                  WIN_FOLDER_DIR, WORDS_FILE_DIR)
from term.exceptions import Lose, Win
from term.filter import Filter
from term.logger import clear_handlers, get_loggers
from term.page.elements import Cell, Term
from term.utils import (create_project_folders, get_driver, get_words_list,
                        move_file_logs, save_screen_image)


class Crawler:
    def __init__(self, page_elements: Term) -> None:
        self.page = page_elements

    @classmethod
    def send_letters_in_cells(cls, cells: List[WebElement], word: List) -> None:
        [cell.send_keys(letter) for cell, letter in zip(cells, word)]

    @classmethod
    def check_win(cls, attributes: List[Cell]) -> bool:
        for attribute in attributes:
            if 'correta' not in attribute.result:
                return False
        return True

    def run(self):
        boards = self.page.get_boards()
        for number, board in enumerate(boards):
            words_list = get_words_list(WORDS_FILE_DIR)
            logger = get_loggers(LOGS_FOLDER_DIR, number)
            filter = Filter(words_list, logger)
            rows = self.page.get_rows(board)
            for number, row in enumerate(rows):
                if not row.text:
                    word = filter.get_random_word()
                    logger.info(f'word: {word}')
                    cells = self.page.get_cells(row)
                    self.send_letters_in_cells(cells, list(word))
                    self.page.confirm_word()
                    attributes = self.page.get_webelements_attribute(cells)
                    if self.check_win(attributes):
                        logger.info('Win!')
                        break
                    filter.filter_words_list(attributes)
                else:
                    cells = self.page.get_cells(row)
                    word = self.page.get_word_in_cells(cells)
                    logger.info(f'word: {word.lower()}')
                    attributes = self.page.get_webelements_attribute(cells)
                    if self.check_win(attributes):
                        logger.info('Win!')
                        break
                    filter.filter_words_list(attributes)
            else:
                logger.info('Lose!')
                raise Lose
        raise Win


if __name__ == '__main__':
    try:
        create_project_folders()
        driver = get_driver()
        crawler = Crawler(Term(driver))
        result = crawler.run()
    except BdbQuit:
        pass
    except Win:
        print('Win!')
        clear_handlers()
        move_file_logs(WIN_FOLDER_DIR)
        input('Send any key to exit \n')
    except Lose:
        print('Lose!')
        clear_handlers()
        folder_logs_path = move_file_logs(LOSE_FOLDER_DIR)
        save_screen_image(folder_logs_path, driver)
        input('Send any key to exit \n')
    except Exception:
        print('Error!')
        clear_handlers()
        error = traceback.format_exc()
        folder_logs_path = move_file_logs(ERROR_FOLDER_DIR, error=error)
        save_screen_image(folder_logs_path, driver)
        input('Send any key to exit \n')
    finally:
        driver.quit()
