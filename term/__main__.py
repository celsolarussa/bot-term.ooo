import traceback
from bdb import BdbQuit
from typing import List

from selenium.webdriver.remote.webelement import WebElement

from term import (
    ERROR_FOLDER_DIR,
    LOGS_FOLDER_DIR,
    LOSE_FOLDER_DIR,
    WIN_FOLDER_DIR,
    WORDS_FILE_DIR,
    utils,
)
from term.exceptions import Lose, Win
from term.filter import Filter
from term.logger import clear_handlers, get_loggers
from term.page.elements import Term


class BoardWebElement:
    def __init__(
        self, page: Term, board: WebElement, board_number: int
    ) -> None:
        self.actual_row_index = 0
        self.page = page
        self.board = board
        self.board_number = board_number
        self.filter = self.get_filter_instance()
        self.len_words_list = len(self.filter.words_list)

    def __lt__(self, other):
        return self.len_words_list < other.len_words_list

    def __repr__(self):
        return f'Board {self.board_number}: {self.len_words_list} words'

    def get_filter_instance(self):
        words_list = utils.get_words_list(WORDS_FILE_DIR)
        logger = get_loggers(LOGS_FOLDER_DIR, self.board_number)
        return Filter(words_list, logger)

    def get_row_by_index(self, aux: int = 0) -> WebElement:
        return self.page.get_rows(self.board)[self.actual_row_index - aux]

    def _send_letters_in_cells(
        self, cells: List[WebElement], word: List[str]
    ) -> None:
        [cell.send_keys(letter) for cell, letter in zip(cells, word)]
        self.page.confirm_word()

    def send_letters_in_cells(self) -> None:
        random_word = self.filter.get_random_word()
        row = self.get_row_by_index()
        cells = self.page.get_cells(row)
        self._send_letters_in_cells(cells, list(random_word))

    def check_correct_word(self) -> bool:
        row = self.get_row_by_index(1)
        cells = self.page.get_cells(row)
        attributes = self.page.get_webelements_attribute(cells)
        for attribute in attributes:
            if 'correta' not in attribute.result:
                return False
        self.filter.logger.info('Correct word!')
        return True

    def filter_words_list(self) -> None:
        row = self.get_row_by_index()
        cells = self.page.get_cells(row)
        attributes = self.page.get_webelements_attribute(cells)
        self.filter.filter_words_list(attributes)
        self.len_words_list = len(self.filter.words_list)
        self.actual_row_index += 1


class Crawler:
    def __init__(self, page_elements: Term) -> None:
        self.page = page_elements
        self.url_page = 'https://term.ooo/4'

    def run(self):
        self.page._driver.get(self.url_page)
        self.page.close_help_screen()
        list_boards = self.page.get_boards()
        board_instances = [
            BoardWebElement(self.page, board, board_number)
            for board_number, board in enumerate(list_boards)]

        row = self.page.get_rows(board_instances[-1].board)
        for i in range(len(row)):
            board = min(board_instances)
            board.send_letters_in_cells()
            [board.filter_words_list() for board in board_instances]
            correct_word = board.check_correct_word()
            if correct_word:
                board_instances.remove(board)
            if not board_instances:
                raise Win
        raise Lose


if __name__ == '__main__':
    try:
        utils.create_project_folders()
        driver = utils.get_driver()
        crawler = Crawler(Term(driver))
        result = crawler.run()
    except Win:
        print('Win!')
        clear_handlers()
        utils.move_file_logs(WIN_FOLDER_DIR)
        input('Send any key to exit \n')
    except Lose:
        print('Lose!')
        clear_handlers()
        folder_logs_path = utils.move_file_logs(LOSE_FOLDER_DIR)
        utils.save_image_screen(folder_logs_path, driver)
        input('Send any key to exit \n')
    except BdbQuit:
        clear_handlers()
        folder_logs_path = utils.move_file_logs(ERROR_FOLDER_DIR)
    except Exception as ex:
        print(f'Error!: {ex}')
        clear_handlers()
        error = traceback.format_exc()
        folder_logs_path = utils.move_file_logs(ERROR_FOLDER_DIR, error=error)
        utils.save_image_screen(folder_logs_path, driver)
        input('Send any key to exit \n')
    finally:
        driver.quit()
