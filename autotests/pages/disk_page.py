import allure
from selenium.webdriver.common.by import By

from autotests.pages.base_page import BasePage


class DiskPage(BasePage):
    FLAG_DISK_PAGE: tuple = (By.XPATH, '//a[contains(@class, "PSHeaderService_active")]/span[text()="Диск"]')
    DESIRED_FILE: tuple = (By.XPATH, '//div[@class="listing__items"]//div[@aria-label="name_file-&"]')
    FOLDER_TITLE: tuple = (By.XPATH, '//div[@class="listing-heading__title-inner"]')

    @allure.step('Проверить, что открылась страница Яндекс Диска')
    def assert_open_disk_page(self, timeout: int = 20) -> None:
        self._find_element(locator=self.FLAG_DISK_PAGE, timeout=timeout)

    @allure.step("Нажать на файл или папку '{name_file}'")
    def click_file(self, name_file: str, timeout: int = 5) -> None:
        self._click(
            locator=(self.DESIRED_FILE[0], self.DESIRED_FILE[1].replace('name_file-&', name_file)), timeout=timeout
        )

    @allure.step("Выделить файлы или папки '{names_files}'")
    def select_files_ctrl(self, names_files: list, timeout: int = 5) -> None:
        locators = []
        for name_file in names_files:
            locators.append((self.DESIRED_FILE[0], self.DESIRED_FILE[1].replace('name_file-&', name_file)))
        self._select_files(locators=locators, timeout=timeout)

    @allure.step("Найти файл или папку '{name_file}'")
    def assert_file(self, name_file: str, timeout: int = 5) -> None:
        self._find_element(
            locator=(self.DESIRED_FILE[0], self.DESIRED_FILE[1].replace('name_file-&', name_file)), timeout=timeout
        )

    @allure.step("Найти файлы или папки '{names_files}'")
    def assert_files(self, names_files: str, timeout: int = 5) -> None:
        for name_file in names_files:
            self.assert_file(name_file=name_file, timeout=timeout)

    @allure.step("Перейти в папку или открыть файл '{name_folder}'")
    def goto_folder(self, name_folder: str, timeout: int = 5) -> None:
        self._double_click(
            locator=(self.DESIRED_FILE[0], self.DESIRED_FILE[1].replace('name_file-&', name_folder)), timeout=timeout
        )

    @allure.step("Проверить, что открылась директория '{name_folder}'")
    def assert_open_folder(self, name_folder: str, timeout: int = 10) -> None:
        self._assert_text_in_element_equal_to(locator=self.FOLDER_TITLE, text=name_folder, timeout=timeout)

    @allure.step("Проверить, что файла (или папки) '{name_file}' нет")
    def assert_desired_file_absence(self, name_file: str, timeout: int = 10) -> None:
        self._assert_quantity_of_elements(
            locator=(self.DESIRED_FILE[0], self.DESIRED_FILE[1].replace('name_file-&', name_file)),
            quantity=0,
            timeout=timeout,
        )

    @allure.step("Проверить, что файлов (или папок) '{names_files}' нет")
    def assert_desired_files_absence(self, names_files: list, timeout: int = 10) -> None:
        for name_file in names_files:
            self.assert_desired_file_absence(name_file=name_file, timeout=timeout)
