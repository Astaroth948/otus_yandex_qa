from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from autotests.pages.disk_page import DiskPage
from autotests.pages.elements.action_bar import ActionBar
from autotests.pages.elements.disk_left_panel import DiskLeftPanel
from autotests.pages.elements.modal import Modal, ModalText
from autotests.pages.elements.notifications import Notifications


def create_folder(driver: WebDriver, name_folder: str) -> None:
    modal = Modal(driver)
    notifications = Notifications(driver)
    disk_left_panel = DiskLeftPanel(driver)
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)

    disk_left_panel.click_create_folder()
    modal.assert_open_modal(title=ModalText.TITLE_CREATE_FOLDER)
    modal.input_name_folder(name_folder=name_folder)
    modal.click_button_save()
    modal.assert_modal_closed()
    notifications.assert_open_toast_create_folder(name_folder=name_folder)
    notifications.click_toast()
    notifications.assert_toast_closed()
    disk_page.assert_file(name_file=name_folder)
    action_bar.click_button_cancel_selection()


def delete_file(driver: WebDriver, name_file: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)

    disk_page.click_file(name_file=name_file)
    action_bar.click_button_delete()
    notifications.assert_open_toast_delete()
    notifications.click_toast()
    notifications.assert_toast_closed()
    disk_page.assert_desired_file_absence(name_file=name_file)


def group_delete_files(driver: WebDriver, names_files: list) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)

    disk_page.select_files_ctrl(names_files=names_files)

    action_bar.click_button_delete()

    notifications.assert_open_toast_delete()
    notifications.click_toast()
    notifications.assert_toast_closed()
    disk_page.assert_desired_files_absence(names_files=names_files)


def upload_file(driver: WebDriver, path_to_file: Path, name_file: str) -> None:
    disk_page = DiskPage(driver)
    notifications = Notifications(driver)
    disk_left_panel = DiskLeftPanel(driver)

    disk_left_panel.upload_file_to_disk(path_to_file=path_to_file)
    notifications.assert_open_uploader()
    notifications.click_close_uploader()
    notifications.assert_uploader_closed()
    disk_page.assert_file(name_file=name_file)


def move_file_in_folder(driver: WebDriver, name_file: str, name_folder: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)
    modal = Modal(driver)

    disk_page.click_file(name_file=name_file)
    action_bar.click_button_move()
    modal.assert_open_modal(title=ModalText.TITLE_MOVE.replace('name_file-&', name_file))
    modal.click_folder(name_folder=name_folder)
    modal.click_button_move()
    modal.assert_modal_closed()

    notifications.assert_open_toast_move(name_file=name_file, name_folder=name_folder)
    notifications.click_toast()
    notifications.assert_toast_closed()
    disk_page.assert_desired_file_absence(name_file=name_file)


def group_move_files_in_folder(driver: WebDriver, names_files: list, name_folder: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)
    modal = Modal(driver)

    disk_page.select_files_ctrl(names_files=names_files)

    action_bar.click_button_move()
    modal.assert_open_modal(title=ModalText.TITLE_GROUP_MOVE.replace('quantity-&', str(len(names_files))))
    modal.click_folder(name_folder=name_folder)
    modal.click_button_move()
    modal.assert_modal_closed()

    notifications.assert_open_toast_group_move(names_files=names_files, name_folder=name_folder)
    notifications.click_toast()
    notifications.assert_toast_closed()
    disk_page.assert_desired_files_absence(names_files=names_files)


def copy_file_in_folder(driver: WebDriver, name_file: str, name_folder: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)
    modal = Modal(driver)

    disk_page.click_file(name_file=name_file)
    action_bar.click_button_copy()
    modal.assert_open_modal(title=ModalText.TITLE_COPY.replace('name_file-&', name_file))
    modal.click_folder(name_folder=name_folder)
    modal.click_button_copy()
    modal.assert_modal_closed()

    notifications.assert_open_toast_copy(name_file=name_file, name_folder=name_folder)
    notifications.click_toast()
    notifications.assert_toast_closed()
    disk_page.assert_file(name_file=name_file)


def group_copy_files_in_folder(driver: WebDriver, names_files: list, name_folder: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    notifications = Notifications(driver)
    modal = Modal(driver)

    disk_page.select_files_ctrl(names_files=names_files)

    action_bar.click_button_copy()
    modal.assert_open_modal(title=ModalText.TITLE_GROUP_COPY.replace('quantity-&', str(len(names_files))))
    modal.click_folder(name_folder=name_folder)
    modal.click_button_copy()
    modal.assert_modal_closed()

    notifications.assert_open_toast_group_copy(names_files=names_files, name_folder=name_folder)
    notifications.click_toast()
    notifications.assert_toast_closed()


def rename_file(driver: WebDriver, old_name: str, new_name: str) -> None:
    disk_page = DiskPage(driver)
    action_bar = ActionBar(driver)
    modal = Modal(driver)

    disk_page.click_file(name_file=old_name)
    action_bar.click_button_rename()
    modal.assert_open_modal(title=ModalText.TITLE_RENAME)
    modal.input_name_folder(name_folder=new_name)
    modal.click_button_save()
    modal.assert_modal_closed()

    disk_page.assert_desired_file_absence(name_file=old_name)
    disk_page.assert_file(name_file=new_name)
