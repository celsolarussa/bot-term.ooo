from typing import List

from pydantic import BaseModel
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from unidecode import unidecode

from term.page.tools import SeleniumTools


class Cell(BaseModel):
    result: str
    position: int

    def __lt__(self, other):
        return tuple(self.dict().values()) < tuple(other.dict().values())


class Term(SeleniumTools):
    div_help_locator = By.ID, 'help'
    wc_board = By.XPATH, '//wc-board'
    wc_rows = By.CSS_SELECTOR, 'wc-row'
    div_letters = By.CSS_SELECTOR, 'div'
    wc_keyboard = By.XPATH, '/html/body/wc-kbd'
    keyboard_enter = By.CSS_SELECTOR, '#kbd_enter'
    div_message = By.ID, 'msg'

    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)

    def close_help_screen(self) -> None:
        self.wait_element_located(locator=self.div_help_locator).click()

    def get_boards(self) -> List[WebElement]:
        return self.find_elements(self.wc_board)

    def get_rows(self, board: WebElement) -> List[WebElement]:
        shadow_wc_board = self.find_shadow_in_webelement(board)
        return self.find_elements_in_webelements(shadow_wc_board, self.wc_rows)

    def get_cells(self, row: WebElement) -> List[WebElement]:
        shadow_wc_rows = self.find_shadow_in_webelement(row)
        return self.find_elements_in_webelements(
            shadow_wc_rows, self.div_letters
        )

    @staticmethod
    def get_word_in_cells(cells: List[WebElement]) -> str:
        return unidecode(''.join([cell.text for cell in cells])).lower()

    def confirm_word(self) -> None:
        webelement = self.find_element(self.wc_keyboard)
        shadow_wc_keyboard = self.find_shadow_in_webelement(webelement)
        self.find_element_in_webelement(
            shadow_wc_keyboard, self.keyboard_enter
        ).click()

    def get_webelements_attribute(self, cells: List) -> list[Cell]:
        return [
            Cell(
                result=self.wait_webelement_attribute(
                    webelement=cell, attr_name='aria-label'
                ),
                position=self.wait_webelement_attribute(
                    webelement=cell, attr_name='termo-pos'
                ),
            )
            for cell in cells
        ]
