import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.disk_page import DiskPage
from pages.elements.disk_left_panel import DiskLeftPanel
from tests.conftest import create_folder, delete_file, group_copy_files_in_folder, group_delete_files

FOLDER: str = 'TestFolder456'
FILES = ['Горы.jpg', 'Зима.jpg', 'Мишки.jpg']


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки создания и удаления')
@allure.suite('Проверки создания и удаления')
@allure.title('Проверка группового удаления файлов')
@pytest.mark.usefixtures('authorization')
def test_group_delete_files(driver: WebDriver) -> None:
    disk_page = DiskPage(driver)
    disk_left_panel = DiskLeftPanel(driver)

    create_folder(driver=driver, name_folder=FOLDER)

    group_copy_files_in_folder(driver=driver, names_files=FILES, name_folder=FOLDER)
    disk_page.goto_folder(name_folder=FOLDER)
    disk_page.assert_open_folder(name_folder=FOLDER)
    disk_page.assert_files(names_files=FILES)

    group_delete_files(driver=driver, names_files=FILES)

    disk_left_panel.goto_files()
    disk_page.assert_open_folder(name_folder='Файлы')

    delete_file(driver=driver, name_file=FOLDER)
