from typing import List

from pydantic import BaseModel
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By

from term.tools import Page, SeleniumTools


class Row(BaseModel):
    cells: list


class Term(SeleniumTools):
    url = 'https://term.ooo/'
    div_help_locator = By.ID, 'help'
    div_rows = By.XPATH, '//*[@id="board"]/div'
    div_cells = By.XPATH, './div'
    button_enter = By.ID, 'kbd_enter'

    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)
        Page.open(driver, self.url)
        self.close_help_screen()

    def close_help_screen(self) -> None:
        self.wait_element_located(locator=self.div_help_locator).click()

    def get_table_rows(self) -> List[Row]:
        webelements = self.find_elements(self.div_rows)
        return [
            Row(cells=self.find_elements_in_webelements(i, self.div_cells))
            for i in webelements
        ]

    def confirm_word(self) -> None:
        self.find_element(self.button_enter).click()

    def get_webelements_attribute(self, webelements: List) -> List[str]:
        return [
            self.wait_webelement_attribute(webelement=ele)
            for ele in webelements
        ]
