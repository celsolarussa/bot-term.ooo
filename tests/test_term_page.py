from selenium.webdriver.common.by import By

from term.page.elements import Term


def test_close_help_screen(driver):
    page = Term(driver)
    assert page


def test_get_all_rows_from_page(driver):
    expected = 6
    page = Term(driver)
    rows = page.get_rows()
    assert len(rows) == expected


def test_get_all_cells_in_row_from_page(driver):
    expected = 5
    div_letters = By.CSS_SELECTOR, 'div'

    page = Term(driver)
    row = page.get_rows()[0]
    shadow_wc_rows = page.find_shadow_in_webelement(row)
    cells = page.find_elements_in_webelements(shadow_wc_rows, div_letters)
    assert len(cells) == expected
