import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ActionBar(BasePage):
    BUTTON_COPY: tuple = (By.XPATH, '//button[@aria-label="Копировать"]')
    BUTTON_DELETE: tuple = (By.XPATH, '//button[@aria-label="Удалить"]')
    BUTTON_MOVE: tuple = (By.XPATH, '//button[@aria-label="Переместить"]')
    BUTTON_RENAME: tuple = (By.XPATH, '//button[@aria-label="Переименовать"]')
    BUTTON_CANCEL_SELECTION: tuple = (By.XPATH, '//button[@aria-label="Отменить выделение"]')
    BUTTON_INFO: tuple = (By.XPATH, '//button[@aria-label="Информация"]')

    @allure.step("Нажать на кнопку 'Копировать'")
    def click_button_copy(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_COPY, timeout=timeout)

    @allure.step("Нажать на кнопку 'Удалить'")
    def click_button_delete(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_DELETE, timeout=timeout)

    @allure.step("Нажать на кнопку 'Переместить'")
    def click_button_move(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_MOVE, timeout=timeout)

    @allure.step("Нажать на кнопку 'Переименовать'")
    def click_button_rename(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_RENAME, timeout=timeout)

    @allure.step("Нажать на кнопку 'Отменить выделение'")
    def click_button_cancel_selection(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_CANCEL_SELECTION, timeout=timeout)

    @allure.step("Нажать на кнопку 'Копировать'")
    def click_button_info(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_INFO, timeout=timeout)
