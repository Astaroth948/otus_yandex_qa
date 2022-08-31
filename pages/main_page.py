import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    BUTTON_AUTH: tuple = (By.XPATH, '//a[@data-statlog="notifications.mail.logout.enter"]')
    BUTTON_MAIL: tuple = (By.XPATH, '//a[text()="Почта"]')
    BUTTON_DISK: tuple = (By.XPATH, '//a[text()="Диск"]')
    FLAG_MAIN_PAGE: tuple = (By.XPATH, '//div[@class="home-logo home-arrow__logo"]')
    USER_PROFILE: tuple = (By.XPATH, '//a[@data-statlog="notifications.mail.login.usermenu.toggle"]')
    BUTTON_EXIT: tuple = (By.XPATH, '//a[@aria-label="Выйти"]')

    @allure.step('Проверить, что открылась главная страница Яндекса')
    def assert_open_main_page(self, timeout: int = 20) -> None:
        self._find_element(locator=self.FLAG_MAIN_PAGE, timeout=timeout)

    @allure.step('Перейти на страницу авторизации')
    def goto_auth_page(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_AUTH, timeout=timeout)

    @allure.step('Перейти на страницу Диска')
    def goto_disk_page(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_DISK, timeout=timeout)

    @allure.step('Нажать на профиль пользователя')
    def click_user_profile(self, timeout: int = 5) -> None:
        self._click(locator=self.USER_PROFILE, timeout=timeout)

    @allure.step('Нажать на кнопку "Выйти"')
    def click_logout(self, timeout: int = 5) -> None:
        self._click(locator=self.BUTTON_EXIT, timeout=timeout)

    @allure.step('Проверить, что пользователь не авторизован')
    def assert_logout(self, timeout: int = 5) -> None:
        self._find_element(locator=self.BUTTON_AUTH, timeout=timeout)
