from dataclasses import dataclass

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Notifications(BasePage):
    NOTIFICATION: tuple = (By.XPATH, '//div[@class="notifications__text js-message"]')
    INFO_NOTIFICATION: tuple = (By.XPATH, '//div[@class="resources-info-dropdown__popup"]')
    UPLOADER_TITLE: tuple = (By.XPATH, '//div[@class="uploader-progress"]//h3')
    UPLOADER_CLOSE: tuple = (By.XPATH, '//div[@class="uploader-progress"]//button[@aria-label="Закрыть"]')
    INFO_NOTIFICATION_FIELD: tuple = (
        By.XPATH,
        '//div[@class="resources-info-dropdown__popup"]//'
        'span[normalize-space(text())="field-&"]/following-sibling::span',
    )

    @allure.step('Проверить, что появилось оповещение об окончании копирования')
    def assert_open_toast_copy(self, name_file: str, name_folder: str, timeout: int = 30) -> None:
        self._assert_text_in_element_equal_to(
            locator=self.NOTIFICATION,
            text=ToastsText.TOAST_COPY.replace('name_file-&', name_file).replace('name_folder-&', name_folder),
            timeout=timeout,
        )

    @allure.step('Проверить, что появилось оповещение об окончании группового копирования')
    def assert_open_toast_group_copy(self, names_files: list, name_folder: str, timeout: int = 30) -> None:
        self._assert_text_in_element_equal_to(
            locator=self.NOTIFICATION,
            text=ToastsText.TOAST_GROUP_COPY.replace('quantity-&', str(len(names_files))).replace(
                'name_folder-&', name_folder
            ),
            timeout=timeout,
        )

    @allure.step('Проверить, что появилось оповещение об окончании перемещения')
    def assert_open_toast_move(self, name_file: str, name_folder: str, timeout: int = 30) -> None:
        self._assert_text_in_element_equal_to(
            locator=self.NOTIFICATION,
            text=ToastsText.TOAST_MOVE.replace('name_file-&', name_file).replace('name_folder-&', name_folder),
            timeout=timeout,
        )

    @allure.step('Проверить, что появилось оповещение об окончании группового перемещения')
    def assert_open_toast_group_move(self, names_files: list, name_folder: str, timeout: int = 30) -> None:
        self._assert_text_in_element_equal_to(
            locator=self.NOTIFICATION,
            text=ToastsText.TOAST_GROUP_MOVE.replace('quantity-&', str(len(names_files))).replace(
                'name_folder-&', name_folder
            ),
            timeout=timeout,
        )

    @allure.step('Проверить, что появилось оповещение о создании папки')
    def assert_open_toast_create_folder(self, name_folder: str, timeout: int = 30) -> None:
        self._assert_text_in_element_equal_to(
            locator=self.NOTIFICATION,
            text=ToastsText.TOAST_CREATE_FOLDER.replace('name_folder-&', name_folder),
            timeout=timeout,
        )

    @allure.step('Проверить, что появилось оповещение об удалении')
    def assert_open_toast_delete(self, timeout: int = 30) -> None:
        self._assert_text_in_element(locator=self.NOTIFICATION, text='Очистить Корзину', timeout=timeout)

    @allure.step('Нажать на оповещение')
    def click_toast(self, timeout: int = 5) -> None:
        self._click(locator=self.NOTIFICATION, timeout=timeout)

    @allure.step('Проверить, что оповещение закрылось')
    def assert_toast_closed(self, timeout: int = 15) -> None:
        self._assert_element_closed(locator=self.NOTIFICATION, timeout=timeout)

    @allure.step('Проверить, что появилось оповещение об окончании загрузки файла')
    def assert_open_uploader(self, timeout: int = 30) -> None:
        self._assert_text_in_element_equal_to(
            locator=self.UPLOADER_TITLE, text=ToastsText.UPLOADER_TITLE, timeout=timeout
        )

    @allure.step('Закрыть оповещение об окончании загрузки файла')
    def click_close_uploader(self, timeout: int = 5) -> None:
        self._click(locator=self.UPLOADER_CLOSE, timeout=timeout)

    @allure.step('Проверить, что оповещение об окончании загрузки файла закрылось')
    def assert_uploader_closed(self, timeout: int = 5) -> None:
        self._assert_element_closed(locator=self.UPLOADER_TITLE, timeout=timeout)

    @allure.step('Проверить, что появилось оповещение с информацией о файле')
    def assert_open_info_notification(self, timeout: int = 30) -> None:
        self._find_element(locator=self.INFO_NOTIFICATION, timeout=timeout)

    @allure.step('Проверить, что поле {field_name} оповещения заполнено {field_value}')
    def assert_field_info_notification(self, field_name: str, field_value: str, timeout: int = 5) -> None:
        self._assert_text_in_element_equal_to(
            locator=(self.INFO_NOTIFICATION_FIELD[0], self.INFO_NOTIFICATION_FIELD[1].replace('field-&', field_name)),
            text=field_value,
            timeout=timeout,
        )

    @allure.step('Проверить, что оповещение с информацией о файле закрылось')
    def assert_info_notification_closed(self, timeout: int = 5) -> None:
        self._assert_element_closed(locator=self.INFO_NOTIFICATION, timeout=timeout)


@dataclass
class ToastsText:
    TOAST_COPY: str = 'Файл «name_file-&» скопирован в папку «name_folder-&»'
    TOAST_CREATE_FOLDER: str = 'Вы создали папку name_folder-&'
    UPLOADER_TITLE: str = 'Все файлы загружены'
    TOAST_MOVE: str = 'Файл «name_file-&» перемещен в «name_folder-&»'
    TOAST_GROUP_MOVE: str = 'Перемещено quantity-& объекта в папку «name_folder-&»'
    TOAST_GROUP_COPY: str = 'Скопировано quantity-& объекта в папку «name_folder-&»'
