from selenium.webdriver import Remote
from selenium.webdriver.common.by import By

from term.page.tools import Page, SeleniumTools


def test_send_driver_and_url_to_open_the_page(driver: Remote):
    expected = 'Termo'
    page_url = 'https://term.ooo/'

    Page.open(driver, page_url)
    assert driver.title == expected


def test_send_element_locator_in_page_and_return_webelement(driver: Remote):
    expected = 'TERMO'
    page_url = 'https://term.ooo/'
    element_locator = By.XPATH, '/html/body/wc-header'

    Page.open(driver, page_url)
    tools = SeleniumTools(driver)
    webelement = tools.wait_element_located(locator=element_locator)
    assert expected in webelement.text


def test_send_locator_in_page_and_return_shadow_element(loaded_page: Remote):
    wc_board_locator = By.XPATH, '/html/body/main/wc-board'

    tools = SeleniumTools(loaded_page)
    webelement = tools.find_element(wc_board_locator)
    shadow_element = tools.find_shadow_in_webelement(webelement)
    assert shadow_element


def test_get_rows_inside_shadow_element(loaded_page: Remote):
    first_wc_board = By.XPATH, '/html/body/main/wc-board'
    second_wc_board_inside_shadow = By.CSS_SELECTOR, 'wc-row'
    expected = 6

    tools = SeleniumTools(loaded_page)
    first_webelement = tools.find_element(first_wc_board)
    first_shadow_element = tools.find_shadow_in_webelement(first_webelement)
    rows = tools.find_elements_in_webelements(
        first_shadow_element, second_wc_board_inside_shadow
    )
    assert len(rows) == expected


def test_get_cells_inside_row(loaded_page: Remote):
    wc_board = By.XPATH, '/html/body/main/wc-board'
    first_row = By.CSS_SELECTOR, 'wc-row:nth-child(2)'
    letters = By.CSS_SELECTOR, 'div'
    expected = 5

    tools = SeleniumTools(loaded_page)
    board_webelement = tools.find_element(wc_board)
    shadow_row = tools.find_shadow_in_webelement(board_webelement)
    row = tools.find_element_in_webelement(shadow_row, first_row)
    shadow_cells = tools.find_shadow_in_webelement(row)
    cells = tools.find_elements_in_webelements(shadow_cells, letters)
    assert len(cells) == expected


def test_send_letter_to_webelement(loaded_page: Remote):
    wc_board = By.XPATH, '/html/body/main/wc-board'
    first_row = By.CSS_SELECTOR, 'wc-row:nth-child(2)'
    letters = By.CSS_SELECTOR, 'div'

    tools = SeleniumTools(loaded_page)
    board_webelement = tools.find_element(wc_board)
    shadow_row = tools.find_shadow_in_webelement(board_webelement)
    row = tools.find_element_in_webelement(shadow_row, first_row)
    shadow_cells = tools.find_shadow_in_webelement(row)
    cell = tools.find_element_in_webelement(shadow_cells, letters)
    cell.send_keys('A')
    assert cell


def test_send_webelement_return_attribute_aria_label_of_the_webelement(
    loaded_page: Remote,
):
    wc_board = By.XPATH, '/html/body/main/wc-board'
    first_row = By.CSS_SELECTOR, 'wc-row:nth-child(2)'
    letters = By.CSS_SELECTOR, 'div'
    expected = ''

    tools = SeleniumTools(loaded_page)
    board_webelement = tools.find_element(wc_board)
    shadow_row = tools.find_shadow_in_webelement(board_webelement)
    row = tools.find_element_in_webelement(shadow_row, first_row)
    shadow_cells = tools.find_shadow_in_webelement(row)
    cell = tools.find_element_in_webelement(shadow_cells, letters)
    attribute = tools.get_webelement_attribute(cell, 'aria-label')
    assert attribute == expected
