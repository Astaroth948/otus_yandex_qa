from typing import Callable

from selenium.common.exceptions import InvalidSelectorException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver


def text_in_element_equal_to(locator: tuple, text_: str) -> Callable[[WebDriver], bool]:
    def _predicate(driver: WebDriver) -> bool:
        try:
            element_text = driver.find_element(*locator).text
            return text_ == element_text
        except InvalidSelectorException as e:
            raise e
        except StaleElementReferenceException:
            return False

    return _predicate


def quantity_of_elements(locator: tuple, quantity: int) -> Callable[[WebDriver], bool]:
    def _predicate(driver: WebDriver) -> bool:
        return len(driver.find_elements(*locator)) == quantity

    return _predicate
