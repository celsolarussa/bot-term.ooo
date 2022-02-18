from pathlib import Path

from term import utils

PROJECT_DIR = Path('.').parent.resolve()


def test_function_returns_word_list():
    expected = 10586
    words_file_path = PROJECT_DIR / 'words.txt'
    words_list = utils.get_words_list(words_file_path)
    assert len(words_list) == expected
