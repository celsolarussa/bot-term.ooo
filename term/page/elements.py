from typing import List

from pydantic import BaseModel
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from term.tools import Page, SeleniumTools


class Row(BaseModel):
    cells: list


class Term(SeleniumTools):
    url = 'https://term.ooo/'
    div_help_locator = By.ID, 'help'
    wc_board = By.XPATH, '/html/body/main/wc-board'
    wc_rows = By.CSS_SELECTOR, 'wc-row'
    div_letters = By.CSS_SELECTOR, 'div'
    wc_keyboard = By.XPATH, '/html/body/wc-kbd'
    keyboard_enter = By.CSS_SELECTOR, '#kbd_enter'
    div_message = By.ID, 'msg'

    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)
        Page.open(driver, self.url)
        self.close_help_screen()

    def close_help_screen(self) -> None:
        self.wait_element_located(locator=self.div_help_locator).click()

    def get_rows(self) -> List[WebElement]:
        webelement = self.find_element(self.wc_board)
        shadow_wc_board = self.find_shadow_in_webelement(webelement)
        return self.find_elements_in_webelements(shadow_wc_board, self.wc_rows)

    def get_cells(self, row: WebElement) -> List[WebElement]:
        shadow_wc_rows = self.find_shadow_in_webelement(row)
        return self.find_elements_in_webelements(
            shadow_wc_rows, self.div_letters
        )

    def get_rows_with_cells(self) -> List[Row]:
        rows = self.get_rows()
        return [Row(cells=self.get_cells(row)) for row in rows]

    def confirm_word(self) -> None:
        webelement = self.find_element(self.wc_keyboard)
        shadow_wc_keyboard = self.find_shadow_in_webelement(webelement)
        self.find_element_in_webelement(
            shadow_wc_keyboard, self.keyboard_enter
        ).click()

    def get_webelements_attribute(self, webelements: List) -> List[str]:
        return [
            self.wait_webelement_attribute(webelement=ele)
            for ele in webelements
        ]
