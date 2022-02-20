from abc import ABC
from typing import Tuple

from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumTools:
    def __init__(self, driver: Remote) -> None:
        self._driver = driver

    def wait_element_located(
        self, time: float = 5.0, locator: Tuple[str, str] = None
    ) -> WebElement:
        return WebDriverWait(self._driver, time).until(
            EC.presence_of_element_located((locator))
        )

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        return self._driver.find_element(*locator)

    def find_elements(self, locator: Tuple[str, str]) -> WebElement:
        return self._driver.find_elements(*locator)

    def find_elements_in_webelements(
        self, webelement: WebElement, locator: Tuple[str, str]
    ) -> WebElement:
        new_webelement = webelement.find_elements(*locator)
        return new_webelement

    def get_webelement_attribute(
        self, webelement: WebElement, attr_name: str = 'aria-label'
    ) -> str:
        return webelement.get_attribute(attr_name)

    def wait_webelement_attribute(
        self, time: float = 5.0, webelement: WebElement = None
    ) -> str:
        return WebDriverWait(self._driver, time).until(
            lambda x: self.get_webelement_attribute(webelement)
        )


class Page(ABC):
    @staticmethod
    def open(driver: Remote, page_url: str) -> None:
        driver.get(page_url)
