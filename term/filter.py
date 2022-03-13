import logging
import re
from random import choice
from typing import List

from unidecode import unidecode

from term.exceptions import FilterError
from term.page.elements import Cell


class LetterCorrectPosition:
    def filtrate(
        self,
        position: int,
        letter: str,
        words_list: List[str],
        pattern_correct: List[str],
        another_position: List[str],
        logger: logging,
    ) -> None:
        pattern_correct[position] = letter
        regex = re.compile(''.join(pattern_correct))
        words_list = list(filter(regex.match, words_list.copy()))
        logger.info(f'letter: {letter}, type: correct, filtered: {words_list}')
        return words_list, pattern_correct, another_position


class LetterAnotherPosition:
    def filtrate(
        self,
        position: int,
        letter: str,
        words_list: List[str],
        pattern_correct: List[str],
        another_position: List[str],
        logger: logging,
    ) -> None:
        # another_position[position] = letter
        another_position.append(
            letter
        ) if letter not in another_position else None
        words_list = list(
            filter(
                lambda x: letter in x and x[position] != letter,
                words_list.copy(),
            )
        )
        logger.info(
            f'letter: {letter}, type: another position, filtered: {words_list}'
        )
        return words_list, pattern_correct, another_position


class WrongLetter:
    def filtrate(
        self,
        position: int,
        letter: str,
        words_list: List[str],
        pattern_correct: List[str],
        another_position: List[str],
        logger: logging,
    ) -> None:
        if letter not in pattern_correct and letter not in another_position:
            words_list = list(
                filter(lambda x: letter not in x, words_list.copy())
            )
        elif letter not in pattern_correct and letter in another_position:
            # possibilidade de conter mais de um elemento dentro da lista
            # de another position, usar dict[position, value]
            count_letter = another_position.count(letter)
            words_list = list(
                filter(
                    lambda x: x[position] != letter
                    and x.count(letter) == count_letter,
                    words_list.copy(),
                )
            )
        elif letter in pattern_correct:
            words_list = list(
                filter(lambda x: x[position] != letter, words_list.copy())
            )
        logger.info(
            f'letter: {letter}, type: wrong letter, filtered: {words_list}'
        )
        return words_list, pattern_correct, another_position


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
    def __init__(self, words_list: List[str], logger: logging) -> None:
        self.words_list = words_list
        self.logger = logger
        self.pattern_correct = [r'\w'] * 5
        self.another_position = []

    def get_random_word(self) -> str:
        if not self.words_list:
            raise FilterError()
        word_list = (
            [i for i in self.words_list.copy() if 'a' in i]
            if len(self.words_list) == 10586
            else self.words_list
        )
        word = choice(word_list)
        self.words_list.remove(word)
        return word

    def get_letter_in_word(
        self, attribute: str, pattern: str = r'"(\w)"'
    ) -> str:
        return unidecode(re.search(pattern, attribute).groups()[0]).lower()

    def filter_words_list(self, attributes: List[Cell]) -> None:
        attributes.sort()
        for attribute in attributes:
            result = attribute.result
            position = attribute.position
            letter = self.get_letter_in_word(result)
            filter_type = result.split(' ')[-1]
            (
                self.words_list,
                self.pattern_correct,
                self.another_position,
            ) = FilterFactory.generate(filter_type).filtrate(
                position,
                letter,
                self.words_list,
                self.pattern_correct,
                self.another_position,
                self.logger,
            )
