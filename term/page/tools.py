from abc import ABC
from typing import List, Tuple

from selenium.webdriver import Remote
from selenium.webdriver.remote.shadowroot import ShadowRoot
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
            EC.presence_of_element_located(locator)
        )

    def find_shadow_in_webelement(self, webelement: WebElement) -> ShadowRoot:
        script = 'return arguments[0].shadowRoot'
        return self._driver.execute_script(script, webelement)

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        return self._driver.find_element(*locator)

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        return self._driver.find_elements(*locator)

    @classmethod
    def find_element_in_webelement(
        cls, webelement: WebElement, locator: Tuple[str, str]
    ) -> WebElement:
        new_webelement = webelement.find_element(*locator)
        return new_webelement

    @classmethod
    def find_elements_in_webelements(
        cls, webelement: WebElement, locator: Tuple[str, str]
    ) -> List[WebElement]:
        new_webelement = webelement.find_elements(*locator)
        return new_webelement

    @classmethod
    def get_webelement_attribute(
        cls, webelement: WebElement, attr_name: str
    ) -> str:
        return webelement.get_attribute(attr_name)

    def wait_webelement_attribute(
        self,
        time: float = 10.0,
        webelement: WebElement = None,
        attr_name: str = None,
    ) -> str:
        return WebDriverWait(self._driver, time).until(
            lambda x: self.get_webelement_attribute(webelement, attr_name)
        )


class Page(ABC):
    @staticmethod
    def open(driver: Remote, page_url: str) -> None:
        driver.get(page_url)
