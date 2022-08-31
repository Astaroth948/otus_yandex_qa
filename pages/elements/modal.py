from dataclasses import dataclass

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Modal(BasePage):
    MODAL_TITLE: tuple = (By.XPATH, '//div[@class="Modal-Content"]//h2')
    MODAL_FOLDER_NAME: tuple = (By.XPATH, '//div[@class="Modal-Content"]//div[@title="name_folder-&"]')
    BUTTON_COPY: tuple = (By.XPATH, '//div[@class="Modal-Content"]//button/span[text()="Копировать"]/parent::button')
    BUTTON_MOVE: tuple = (By.XPATH, '//div[@class="Modal-Content"]//button/span[text()="Переместить"]/parent::button')
    INPUT_CREATE_FOLDER: tuple = (By.XPATH, '//div[@class="Modal-Content"]//input')
    BUTTON_SAVE: tuple = (By.XPATH, '//div[@class="Modal-Content"]//button/span[text()="Сохранить"]/parent::button')
    NAME_ERROR: tuple = (By.XPATH, '//div[@class="Modal-Content"]//div[@class="rename-dialog__rename-error"]')
    BUTTON_CLOSE: tuple = (By.XPATH, '//div[@class="Modal-Content"]//button[@aria-label="Закрыть"]')

    @allure.step('Проверить, что открылось модальное окно с заголовком {title}')
    def assert_open_modal(self, title: str, timeout: int = 5) -> None:
        self._assert_text_in_element_equal_to(locator=self.MODAL_TITLE, text=title, timeout=timeout)

    @allure.step('Проверить, что модальное окно закрылось')
    def assert_modal_closed(self, timeout: int = 5) -> None:
        self._assert_element_closed(locator=self.MODAL_TITLE, timeout=timeout)

    @allure.step("Нажать на директорию: '{name_folder}' в модальном окне")
    def click_folder(self, name_folder: str, timeout: int = 5) -> None:
        self._click(
            locator=(self.MODAL_FOLDER_NAME[0], self.MODAL_FOLDER_NAME[1].replace('name_folder-&', name_folder)),
            timeout=timeout,
        )

    @allure.step("Нажать на кнопку 'Копировать' в модальном окне")
    def click_button_copy(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_COPY, timeout=timeout)

    @allure.step("Ввести название папки: '{name_folder}'")
    def input_name_folder(self, name_folder: str, timeout: int = 5) -> None:
        self._clear_input(locator=self.INPUT_CREATE_FOLDER, timeout=timeout)
        self._input_text(locator=self.INPUT_CREATE_FOLDER, text=name_folder, timeout=timeout)

    @allure.step("Нажать на кнопку 'Сохранить' в модальном окне")
    def click_button_save(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_SAVE, timeout=timeout)

    @allure.step("Нажать на кнопку 'Переместить' в модальном окне")
    def click_button_move(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_MOVE, timeout=timeout)

    @allure.step("Нажать на кнопку 'Закрыть' в модальном окне")
    def click_button_close(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_CLOSE, timeout=timeout)

    @allure.step('Проверить, что появилась ошибка, что папка с таким именем уже существует')
    def assert_error_name_folder(self, name_folder: str, timeout: int = 5) -> None:
        self._find_element(
            locator=(self.NAME_ERROR[0], self.NAME_ERROR[1].replace('name_folder-&', name_folder)), timeout=timeout
        )


@dataclass
class ModalText:
    TITLE_COPY: str = 'Куда копировать «name_file-&»?'
    TITLE_MOVE: str = 'Куда переместить «name_file-&»?'
    TITLE_GROUP_MOVE: str = 'Куда переместить quantity-& объекта?'
    TITLE_GROUP_COPY: str = 'Куда копировать quantity-& объекта?'
    TITLE_CREATE_FOLDER: str = 'Укажите название папки'
    TITLE_RENAME: str = 'Переименовать'
    ERROR_RENAME: str = 'Папка с именем «name_folder-&» уже существует'
