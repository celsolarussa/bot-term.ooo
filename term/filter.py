import logging
import re
from random import choice
from typing import List

from unidecode import unidecode

from term import WORDS_FILE_DIR
from term.exceptions import FilterError
from term.utils import get_words_list

WORDS_LIST = get_words_list(WORDS_FILE_DIR)
PATTERN_CORRECT = [r'\w'] * 5
ANOTHER_POSITION = []


class LetterCorrectPosition:
    def filtrate(self, position: int, letter: str) -> None:
        global PATTERN_CORRECT, WORDS_LIST

        PATTERN_CORRECT[position] = letter
        regex = re.compile(''.join(PATTERN_CORRECT))
        WORDS_LIST = list(filter(regex.match, WORDS_LIST.copy()))
        logging.info(
            f'letter: {letter}, type: correct, filtered: {WORDS_LIST}'
        )


class LetterAnotherPosition:
    def filtrate(self, position: int, letter: str) -> None:
        global ANOTHER_POSITION, WORDS_LIST

        ANOTHER_POSITION.append(letter)
        WORDS_LIST = list(
            filter(
                lambda x: letter in x and x[position] != letter,
                WORDS_LIST.copy(),
            )
        )
        logging.info(
            f'letter: {letter}, type: another position, filtered: {WORDS_LIST}'
        )


class WrongLetter:
    def filtrate(self, position: int, letter: str) -> None:
        global PATTERN_CORRECT, ANOTHER_POSITION, WORDS_LIST

        if letter not in PATTERN_CORRECT and letter not in ANOTHER_POSITION:
            callable = lambda x: letter not in x
        elif letter not in PATTERN_CORRECT and letter in ANOTHER_POSITION:
            count_letter = ANOTHER_POSITION.count(letter)
            callable = (
                lambda x: x[position] != letter
                and x.count(letter) == count_letter
            )
        elif letter in PATTERN_CORRECT:
            callable = lambda x: x[position] != letter
        WORDS_LIST = list(filter(callable, WORDS_LIST.copy()))
        logging.info(
            f'letter: {letter}, type: wrong letter, filtered: {WORDS_LIST}'
        )


class FilterFactory:
    type = {
        'correta': LetterCorrectPosition,
        'local': LetterAnotherPosition,
        'errada': WrongLetter,
    }

    @staticmethod
    def generate(filter_type: str) -> object:
        return FilterFactory.type[filter_type]()


class Filter:
    def get_random_word(self) -> str:
        if not WORDS_LIST:
            raise FilterError()
        word_list = (
            [i for i in WORDS_LIST.copy() if 'a' in i]
            if len(WORDS_LIST) == 10586
            else WORDS_LIST
        )
        word = choice(word_list)
        WORDS_LIST.remove(word)
        logging.info(f'word: {word}')
        return word

    def get_letter_in_word(
        self, attribute: str, pattern: str = r'"(\w)"'
    ) -> str:
        return unidecode(re.search(pattern, attribute).groups()[0]).lower()

    def filter_words_list(self, attributes: List[str]) -> None:
        for attribute in attributes:
            position = attributes.index(attribute)
            letter = self.get_letter_in_word(attribute)
            filter_type = attribute.split(' ')[-1]
            FilterFactory.generate(filter_type).filtrate(position, letter)
