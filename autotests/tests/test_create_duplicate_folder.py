import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from autotests.pages.elements.disk_left_panel import DiskLeftPanel
from autotests.pages.elements.modal import Modal, ModalText
from autotests.tests.conftest import create_folder, delete_file

NAME_FOLDER: str = 'TestFolder678'


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки создания и удаления')
@allure.suite('Проверки создания и удаления')
@allure.title('Проверка создания дубликата папки')
@pytest.mark.usefixtures('authorization')
def test_create_duplicate_folder(driver: WebDriver) -> None:
    modal = Modal(driver)
    disk_left_panel = DiskLeftPanel(driver)

    create_folder(driver=driver, name_folder=NAME_FOLDER)
    disk_left_panel.click_create_folder()
    modal.assert_open_modal(title=ModalText.TITLE_CREATE_FOLDER)
    modal.input_name_folder(name_folder=NAME_FOLDER)
    modal.assert_error_name_folder(name_folder=NAME_FOLDER)
    modal.click_button_close()
    modal.assert_modal_closed()

    delete_file(driver=driver, name_file=NAME_FOLDER)
