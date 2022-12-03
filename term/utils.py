from datetime import datetime
from pathlib import Path
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from term import (
    ERROR_FOLDER_DIR,
    EXCEPTION_FILE_DIR,
    IMAGE_DIR,
    LOGS_FOLDER_DIR,
    LOSE_FOLDER_DIR,
    RESULT_FOLDER_DIR,
    WIN_FOLDER_DIR,
)


def get_words_list(file_path: Path) -> List[str]:
    with open(file_path, 'r') as f:
        words = f.read()
        return words.split(' ')


def get_driver() -> Chrome:
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--log-level=3')
    driver = Chrome(
        options=options,
    )
    return driver


def create_project_folders() -> None:
    RESULT_FOLDER_DIR.mkdir(exist_ok=True)
    ERROR_FOLDER_DIR.mkdir(exist_ok=True)
    LOSE_FOLDER_DIR.mkdir(exist_ok=True)
    WIN_FOLDER_DIR.mkdir(exist_ok=True)
    LOGS_FOLDER_DIR.mkdir(exist_ok=True)


def get_files_path(folder_path: Path) -> list[Path]:
    files_path = list(Path(folder_path).resolve().iterdir())
    return files_path


def move_file(file_path: Path, file_name: str, destination_path: Path) -> Path:
    _file_path = file_path.rename(destination_path / file_name)
    return _file_path


def move_files(origin_path: Path, destination_path: Path) -> None:
    files_path = get_files_path(origin_path)
    [move_file(i, i.name, destination_path) for i in files_path]


def get_formatted_datetime(prefix: str = '', suffix: str = '') -> str:
    current_day_formatted = (
        str(datetime.now()).replace(':', '.').replace(' ', '_')
    )
    file_name = prefix + current_day_formatted + suffix
    return file_name


def create_folder(destination: Path, folder_name: str) -> Path:
    folder_path = Path(destination / folder_name)
    folder_path.mkdir()
    return folder_path


def move_file_logs(destinaton_path: Path, error: str = None) -> Path:
    logs_folder_name = get_formatted_datetime()
    logs_folder_path = create_folder(destinaton_path, logs_folder_name)
    if error:
        with open(EXCEPTION_FILE_DIR, 'w') as file:
            file.write(error)
        move_file(EXCEPTION_FILE_DIR, EXCEPTION_FILE_DIR.name, LOGS_FOLDER_DIR)
    move_files(LOGS_FOLDER_DIR, logs_folder_path)
    return logs_folder_path


def save_image_screen(destination_path: Path, driver: Chrome):
    driver.save_screenshot(IMAGE_DIR.name)
    move_file(IMAGE_DIR, IMAGE_DIR.name, destination_path)
