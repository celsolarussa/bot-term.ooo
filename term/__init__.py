from pathlib import Path

PROJECT_DIR = Path('.').parent.resolve()
WORDS_FILE_DIR = PROJECT_DIR / 'words.txt'
LOG_FILE_DIR = PROJECT_DIR / 'logs.log'
RESULT_FOLDER_DIR = PROJECT_DIR / 'result'
ERROR_FOLDER_DIR = RESULT_FOLDER_DIR / 'error'
LOSE_FOLDER_DIR = RESULT_FOLDER_DIR / 'lose'
WIN_FOLDER_DIR = RESULT_FOLDER_DIR / 'win'
