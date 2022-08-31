from typing import Generator

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera import options as OperaOptions
from selenium.webdriver.remote.webdriver import WebDriver

from pages.auth_page import AuthPage, AuthPageText
from pages.disk_page import DiskPage
from pages.main_page import MainPage
from types import AuthData


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--url', action='store', default='https://yandex.ru/', help='URL адрес тестируемой страницы')
    parser.addoption('--login', action='store', default=None, help='Логин')
    parser.addoption('--password', action='store', default=None, help='Пароль')
    parser.addoption('--headless', action='store_true')
    parser.addoption('--browser', action='store', default='chrome', choices=['chrome', 'firefox', 'opera'])
    parser.addoption('--executor', default='local')
    parser.addoption('--bv', default=None)
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--logs', action='store_true')
    parser.addoption('--videos', action='store_true')


@pytest.fixture(scope='module')
def auth_data(request: FixtureRequest) -> AuthData:
    url = request.config.getoption('--url')
    login = request.config.getoption('--login')
    password = request.config.getoption('--password')
    return AuthData(url=url, login=login, password=password)


@pytest.fixture(scope='module')
def driver(request: FixtureRequest) -> Generator[None, None, None]:
    browser = request.config.getoption('--browser')
    headless = request.config.getoption('--headless')
    executor = request.config.getoption('--executor')
    version = request.config.getoption('--bv')
    vnc = request.config.getoption('--vnc')
    logs = request.config.getoption('--logs')
    videos = request.config.getoption('--videos')

    if executor == 'local':
        if browser == 'chrome':
            options = ChromeOptions()
            options.headless = headless
            options.add_argument('window-size=1920,1080')
            web_driver = webdriver.Chrome(options=options)
        elif browser == 'firefox':
            options = FirefoxOptions()
            options.headless = headless
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
            web_driver = webdriver.Firefox(options=options)
        elif browser == 'opera':
            options = OperaOptions.ChromeOptions()
            options.headless = headless
            options.add_argument('window-size=1920,1080')
            options.add_experimental_option('w3c', True)
            web_driver = webdriver.Opera(options=options)
    else:
        executor_url = f'http://{executor}:4444/wd/hub'
        caps = {
            'browserName': browser,
            'browserVersion': version,
            'name': 'Marat',
            'selenoid:options': {'enableVNC': vnc, 'enableVideo': videos, 'enableLog': logs, 'sessionTimeout': '2m'},
            'acceptSslCerts': True,
            'acceptInsecureCerts': True,
            'timeZone': 'Europe/Moscow',
        }
        options = ChromeOptions()
        options.headless = headless
        options.add_argument('window-size=1920,1080')
        if browser == 'opera':
            options.add_experimental_option('w3c', True)

        web_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=caps, options=options)

    if not headless:
        web_driver.maximize_window()
    web_driver.url = request.config.getoption('--url')

    yield web_driver
    web_driver.quit()


@pytest.fixture(scope='module')
def authorization(driver: WebDriver, auth_data: AuthData) -> Generator[None, None, None]:
    main_page = MainPage(driver)
    auth_page = AuthPage(driver)
    disk_page = DiskPage(driver)

    main_page.open(url=auth_data.url)
    main_page.assert_open_main_page()
    main_page.goto_auth_page()

    auth_page.assert_text_in_header(text=AuthPageText.TITLE_LOGIN)
    auth_page.switch_input_login()
    auth_page.input_login(login=auth_data.login)
    auth_page.click_button_enter()

    auth_page.assert_text_in_header(text=AuthPageText.TITLE_PASSWORD)
    auth_page.assert_current_user_selected(login=auth_data.login)
    auth_page.input_password(password=auth_data.password)
    auth_page.click_button_enter()
    main_page.assert_open_main_page()

    main_page.goto_disk_page()
    main_page._switch_to_new_tab()
    disk_page.assert_open_disk_page()

    yield
    disk_page._close_current_tab()

    main_page.click_user_profile()
    main_page.click_logout()
    main_page.assert_logout()
