import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from autotests.tests.conftest import create_folder, delete_file, rename_file

OLD_NAME: str = 'TestFolder777'
NEW_NAME: str = 'TestFolder555'


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки переименования')
@allure.suite('Проверки переименования')
@allure.title('Проверка переименования папки')
@pytest.mark.usefixtures('authorization')
def test_rename_folder(driver: WebDriver) -> None:
    create_folder(driver=driver, name_folder=OLD_NAME)
    rename_file(driver=driver, old_name=OLD_NAME, new_name=NEW_NAME)
    delete_file(driver=driver, name_file=NEW_NAME)
