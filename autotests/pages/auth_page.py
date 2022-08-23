from dataclasses import dataclass

import allure
from selenium.webdriver.common.by import By

from autotests.pages.base_page import BasePage


class AuthPage(BasePage):
    TITLE: tuple = (By.XPATH, '//h1[@data-t="title"]')
    TAB_MAIL: tuple = (By.XPATH, '//button[@data-type="login"]')
    TAB_PHONE: tuple = (By.XPATH, '//button[@data-type="phone"]')
    INPUT_LOGIN: tuple = (By.XPATH, '//input[@data-t="field:input-login"]')
    INPUT_PASSWORD: tuple = (By.XPATH, '//input[@data-t="field:input-passwd"]')
    BUTTON_ENTER: tuple = (By.XPATH, '//button[@type="submit"]')
    BUTTON_SKIP: tuple = (By.XPATH, '//button[@data-t="button:pseudo"]')
    SELECT_CURRENT_ACCOUNT: tuple = (By.XPATH, '//a[@class="CurrentAccount"]')

    @allure.step("Нажать на кнопку 'Войти'")
    def click_button_enter(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_ENTER, timeout=timeout)

    @allure.step("Нажать на кнопку 'Не сейчас'")
    def click_button_skip(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_SKIP, timeout=timeout)

    @allure.step("Проверить, что заголовок содержит текст '{text}'")
    def assert_text_in_header(self, text: str, timeout: int = 5) -> None:
        self._assert_text_in_element_equal_to(locator=self.TITLE, text=text, timeout=timeout)

    @allure.step("Проверить, что в качестве текщего пользователя выбран '{login}'")
    def assert_current_user_selected(self, login: str, timeout: int = 5) -> None:
        self._assert_text_in_element_equal_to(locator=self.SELECT_CURRENT_ACCOUNT, text=login, timeout=timeout)

    @allure.step("Ввести '{login}' в поле ввода логина")
    def input_login(self, login: str, timeout: int = 5) -> None:
        self._input_text(locator=self.INPUT_LOGIN, text=login, timeout=timeout)

    @allure.step("Ввести '{password}' в поле ввода пароля")
    def input_password(self, password: str, timeout: int = 5) -> None:
        self._input_text(locator=self.INPUT_PASSWORD, text=password, timeout=timeout)

    @allure.step('Переключить способ авторизации на ввод логина')
    def switch_input_login(self, timeout: int = 5) -> None:
        if 'button:clear' in self._get_attribute(locator=self.TAB_MAIL, attribute='data-t', timeout=timeout):
            self._click(locator=self.TAB_MAIL, timeout=timeout)


@dataclass
class AuthPageText:
    TITLE_LOGIN: str = 'Войдите с Яндекс ID'
    TITLE_PASSWORD: str = 'Войдите, чтобы продолжить'
