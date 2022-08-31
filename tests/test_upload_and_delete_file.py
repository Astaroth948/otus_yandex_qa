import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.elements.disk_left_panel import PATH_TO_FILE
from tests.conftest import delete_file, upload_file

FILE: str = 'file.txt'


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки загрузки')
@allure.suite('Проверки загрузки')
@allure.title('Проверка загрузки и удаления файла')
@pytest.mark.usefixtures('authorization')
def test_upload_and_delete_file(driver: WebDriver) -> None:
    upload_file(driver=driver, path_to_file=PATH_TO_FILE, name_file=FILE)
    delete_file(driver=driver, name_file=FILE)
