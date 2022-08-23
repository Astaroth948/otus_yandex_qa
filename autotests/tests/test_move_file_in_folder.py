import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from autotests.pages.disk_page import DiskPage
from autotests.pages.elements.disk_left_panel import PATH_TO_FILE, DiskLeftPanel
from autotests.tests.conftest import create_folder, delete_file, move_file_in_folder, upload_file

FOLDER: str = 'TestFolder'
FILE: str = 'file.txt'


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки перемещения')
@allure.suite('Проверки перемещения')
@allure.title('Проверка перемещения файла')
@pytest.mark.usefixtures('authorization')
def test_move_file_in_folder(driver: WebDriver) -> None:
    disk_page = DiskPage(driver)
    disk_left_panel = DiskLeftPanel(driver)

    upload_file(driver=driver, path_to_file=PATH_TO_FILE, name_file=FILE)
    create_folder(driver=driver, name_folder=FOLDER)

    move_file_in_folder(driver=driver, name_file=FILE, name_folder=FOLDER)
    disk_page.goto_folder(name_folder=FOLDER)
    disk_page.assert_open_folder(name_folder=FOLDER)
    disk_page.assert_file(name_file=FILE)

    disk_left_panel.goto_files()
    disk_page.assert_open_folder(name_folder='Файлы')

    delete_file(driver=driver, name_file=FOLDER)
