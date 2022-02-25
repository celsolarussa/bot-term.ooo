import pytest

from term.page.elements import Term
from term.utils import get_driver


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


@pytest.fixture
def loaded_page(driver):
    Term(driver)
    return driver
