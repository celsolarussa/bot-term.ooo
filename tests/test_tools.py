from selenium.webdriver.common.by import By

from term.tools import Page, SeleniumTools


def test_send_driver_and_url_to_open_the_page(driver):
    expected = 'Termo'
    page_url = 'https://term.ooo/'
    Page.open(driver, page_url)
    assert driver.title == expected


def test_send_element_locator_in_page_and_return_webelement(driver):
    expected = 'TERMO'
    page_url = 'https://term.ooo/'
    element_locator = By.XPATH, '/html/body/header/h1'
    Page.open(driver, page_url)
    tools = SeleniumTools(driver)
    webelement = tools.wait_element_located(locator=element_locator)
    assert webelement.text == expected


def test_send_letter_to_webelement(loaded_page):
    letter = 'A'
    locator = By.XPATH, '//*[@id="board"]/div[1]/div[1]'
    tools = SeleniumTools(loaded_page)
    webelement = tools.find_element(locator)
    webelement.send_keys(letter)
    assert webelement.text == letter


def test_send_webelement_return_attribute_aria_label_of_the_webelement(
    loaded_page,
):
    expected = ''
    locator = By.XPATH, '//*[@id="board"]/div[1]/div[1]'
    tools = SeleniumTools(loaded_page)
    webelement = tools.find_element(locator)
    attribute = tools.get_webelement_attribute(webelement)
    assert attribute == expected
