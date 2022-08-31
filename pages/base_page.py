from pathlib import Path
from typing import List

import allure
import pytest
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tools import new_expected_conditions as NEC


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    @allure.step("Открыть страницу '{url}'")
    def open(self, url: str) -> None:
        self._driver.get(url)

    @allure.step("Найти элемент '{locator}'")
    def _find_element(self, locator: tuple, timeout: int = 5) -> WebElement:
        try:
            element = WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self._fail(f'Не найден элемент {locator}')
        return element

    @allure.step("Найти элементы '{locator}'")
    def _find_elements(self, locator: tuple) -> List[WebElement]:
        return self._driver.find_elements(*locator)

    @allure.step("Проверить, есть элемент '{locator}' на странице")
    def _is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self._driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            return False
        return True

    @allure.step("Проверить, что элемента '{locator}' нет или он закрылся")
    def _assert_element_closed(self, locator: tuple, timeout: int = 5) -> None:
        try:
            WebDriverWait(self._driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            self._fail(f'Элемент {locator} присутствует на странице')

    @allure.step("Нажать на элемент '{locator}'")
    def _click(self, locator: tuple, timeout: int = 5) -> None:
        element = self._find_element(locator=locator, timeout=timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self._fail(f'Элемент {locator} перекрыт')

    @allure.step("Дважды нажать на элемент '{locator}'")
    def _double_click(self, locator: tuple, timeout: int = 5) -> None:
        ActionChains(self._driver).double_click(
            on_element=self._find_element(locator=locator, timeout=timeout)
        ).perform()

    @allure.step("Выделить элементы '{locators}' с нажатым левым CTRL")
    def _select_files(self, locators: str, timeout: int = 5) -> None:
        action = ActionChains(self._driver)
        action.key_down(Keys.LEFT_CONTROL)
        for locator in locators:
            element = self._find_element(locator=locator, timeout=timeout)
            action.click(on_element=element)
        action.key_up(Keys.LEFT_CONTROL).perform()

    @allure.step("Проверить, что текст элемента '{locator}' равен тексту '{text}'")
    def _assert_text_in_element_equal_to(self, locator: tuple, text: str, timeout: int = 5) -> None:
        try:
            WebDriverWait(self._driver, timeout).until(NEC.text_in_element_equal_to(locator, text))
        except TimeoutException:
            self._fail(f'Текст элемента {locator} не равен тексту "{text}"')

    @allure.step("Проверить, что элемент '{locator}' содержит текст {text}")
    def _assert_text_in_element(self, locator: tuple, text: str, timeout: int = 5) -> None:
        try:
            WebDriverWait(self._driver, timeout).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            self._fail(f'Текст элемента {locator} не содержит текст "{text}"')

    @allure.step("Очистить текстовое поле '{locator}'")
    def _clear_input(self, locator: tuple, timeout: int = 5) -> None:
        element = self._find_element(locator=locator, timeout=timeout)
        element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(Keys.DELETE)

    @allure.step("Ввести текст '{text}' в элемент '{locator}'")
    def _input_text(self, locator: tuple, text: str, timeout: int = 5) -> None:
        self._find_element(locator=locator, timeout=timeout).send_keys(text)

    @allure.step("Получить значение атрибута '{attribute}' у элемента '{locator}'")
    def _get_attribute(self, locator: tuple, attribute: str, timeout: int = 5) -> str:
        attribute_value = self._find_element(locator=locator, timeout=timeout).get_attribute(attribute)
        if attribute_value is None:
            pytest.fail(f"Значение атрибута '{attribute}' не найдено у элемента '{locator}'")
        return attribute_value

    @allure.step("Проверить, что кол-во элементов '{locator}' равно {quantity}")
    def _assert_quantity_of_elements(self, locator: tuple, quantity: int, timeout: int = 5) -> None:
        try:
            WebDriverWait(self._driver, timeout).until(NEC.quantity_of_elements(locator, quantity))
        except TimeoutException:
            self._fail(f'Кол-во элементов {locator} не равно {quantity}')

    @allure.step('Переключиться на последнюю вкладку')
    def _switch_to_new_tab(self) -> None:
        self._driver.switch_to.window(self._driver.window_handles[-1])

    @allure.step('Загрузить файл')
    def _upload_file_to_server(self, locator: tuple, path_to_file: Path, timeout: int = 5) -> None:
        element = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located(locator))
        element.send_keys(str(Path(Path.cwd(), path_to_file)))

    @allure.step('Закрыть текщую вкладку')
    def _close_current_tab(self) -> None:
        self._driver.close()
        self._switch_to_new_tab()

    def _fail(self, error_text: str) -> None:
        allure.attach(
            name=self._driver.session_id,
            body=self._driver.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG,
        )
        raise AssertionError(error_text)
