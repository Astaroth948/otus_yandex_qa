import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.disk_page import DiskPage
from pages.elements.disk_left_panel import DiskLeftPanel
from tests.conftest import copy_file_in_folder, create_folder, delete_file

FOLDER: str = 'TestFolder789'
FILE: str = 'Санкт-Петербург.jpg'


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки копирования')
@allure.suite('Проверки копирования')
@allure.title('Проверка копирования файла')
@pytest.mark.usefixtures('authorization')
def test_copy_file_in_folder(driver: WebDriver) -> None:
    disk_page = DiskPage(driver)
    disk_left_panel = DiskLeftPanel(driver)

    create_folder(driver=driver, name_folder=FOLDER)

    copy_file_in_folder(driver=driver, name_file=FILE, name_folder=FOLDER)
    disk_page.goto_folder(name_folder=FOLDER)
    disk_page.assert_open_folder(name_folder=FOLDER)
    disk_page.assert_file(name_file=FILE)

    disk_left_panel.goto_files()
    disk_page.assert_open_folder(name_folder='Файлы')

    delete_file(driver=driver, name_file=FOLDER)
