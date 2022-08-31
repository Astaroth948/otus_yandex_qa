import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.disk_page import DiskPage
from pages.elements.action_bar import ActionBar
from pages.elements.notifications import Notifications


@allure.epic('Проверки Яндекс Диска')
@allure.parent_suite('Проверки Яндекс Диска')
@allure.feature('Проверки просмотра информации')
@allure.suite('Проверки просмотра информации')
@allure.title('Проверка просмотра информации о файле')
@pytest.mark.usefixtures('authorization')
@pytest.mark.parametrize(
    'name_file, size_file, changed_date',
    [
        ('Санкт-Петербург.jpg', '2,4 МБ', '22.08.2022 08:38'),
        ('Москва.jpg', '1,3 МБ', '22.08.2022 08:38'),
        ('Море.jpg', '1 МБ', '22.08.2022 08:38'),
    ],
)
def test_show_file_info(driver: WebDriver, name_file: str, size_file: str, changed_date: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)

    disk_page.click_file(name_file=name_file)
    action_bar.click_button_info()
    notifications.assert_open_info_notification()
    notifications.assert_field_info_notification(field_name='Имя:', field_value=name_file)
    notifications.assert_field_info_notification(field_name='Размер:', field_value=size_file)
    notifications.assert_field_info_notification(field_name='Изменён:', field_value=changed_date)

    action_bar.click_button_info()
    notifications.assert_info_notification_closed()
