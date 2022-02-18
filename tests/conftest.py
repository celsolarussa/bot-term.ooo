import pytest
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options

from term.page.elements import Term


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--start-maximized')
    driver = Remote(
        command_executor='http://127.0.0.1:4444/wd/hub', options=options
    )
    yield driver
    driver.quit()


@pytest.fixture
def loaded_page(driver):
    Term(driver)
    return driver
