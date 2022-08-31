from pathlib import Path

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

PATH_TO_FILE = Path('autotests', 'data', 'file.txt')


class DiskLeftPanel(BasePage):
    FILES: tuple = (By.XPATH, '//div[@class="LeftColumn__InnerWrapperTop"]//span[@id="/disk"]')
    BUTTON_CREATE: tuple = (By.XPATH, '//span[@class="create-resource-popup-with-anchor"]/button')
    BUTTON_CREATE_FOLDER: tuple = (By.XPATH, '//button[@aria-label="Папку"]')
    INPUT_UPLOAD_FILE: tuple = (
        By.XPATH,
        '//div[@class="LeftColumn__InnerWrapperTop"]//input[@title="Загрузить файлы"]',
    )

    @allure.step("Перейти во вкладку 'Файлы' в левом меню")
    def goto_files(self, timeout: int = 5) -> None:
        self._click(locator=self.FILES, timeout=timeout)

    @allure.step("Нажать 'Создать' -> 'Папку' в левом меню")
    def click_create_folder(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_CREATE, timeout=timeout)
        self._click(locator=self.BUTTON_CREATE_FOLDER, timeout=timeout)

    @allure.step('Загрузить файл {path_to_file} в Яндекс Диск')
    def upload_file_to_disk(self, path_to_file: Path, timeout: int = 5) -> None:
        self._upload_file_to_server(locator=self.INPUT_UPLOAD_FILE, path_to_file=path_to_file, timeout=timeout)
