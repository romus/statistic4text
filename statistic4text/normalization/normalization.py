# -*- coding: utf-8 -*-

__author__ = 'romus'

import re
import unicodedata

from ir.stemming.porter_stemmer import PorterStemming
from ir.detection.detection import Detection


class Normalization(object):
    """Нормализация строк"""
    __DIACRITICS = re.compile(u'[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]', re.U)
    __PORTER_ST = PorterStemming()
    __DETECTION = Detection()
    max_len_word = 100        # максимальная длина слова
    min_len_word = 2          # минимальная длина слова

    def __init__(self):
        super(Normalization, self).__init__()

    def __normalize_word(self, word):
        """
        Убрать из начала и конца слова все символы не из алфавита

        :param word: слово
        :return: нормализованное слово
        """

        unicode_word = word
        try:
            unicode_word = word.decode("utf-8")
        except UnicodeEncodeError:
            # print "UnicodeEncodeError"
            pass

        word_len = len(unicode_word)

        if word_len == 0:
            return unicode_word

        f_index = 0             # индекс первого символа
        s_index = word_len - 1  # индекс последнего символа

        # ищем позицию первого индекса
        for x in range(0, word_len):
            f_index = x
            if self.__DETECTION.check_symbol(unicode_word[x]):
                break

        for x in range(s_index, f_index, -1):
            s_index = x
            if self.__DETECTION.check_symbol(unicode_word[x]):
                break

        if f_index + 1 >= s_index:
                return unicode_word[f_index]

        return unicode_word[f_index: s_index + 1]

    def normalize(self, string):
        """
        Вернуть нормализованный список слов:
        1. удалить диакритические знаки;
        2. привести строку к нижнему регистру;
        3. удалить спец-символы
        4. проверка на максимальную/минимальную длину слова
        5. провести стеминг слов, если это возможно;
        6. удалить одинаковые слова.

        >>> norm = Normalization()
        >>> norm.normalize("Это простая проверка") # ['эт', 'прост', 'проверк']
        [u'\u044d\u0442', u'\u043f\u0440\u043e\u0441\u0442', u'\u043f\u0440\u043e\u0432\u0435\u0440\u043a']
        >>> norm.normalize("This is only testing")
        [u'thi', u'is', u'onli', u'test']
        >>> norm.normalize("   This   is   only   test   a")
        [u'thi', u'is', u'onli', u'test']
        """

        normalize_string = None
        try:
            normalize_string = self.__DIACRITICS.sub('', unicodedata.normalize('NFD', unicode(string, "UTF-8")))
            # normalize_string = self.__DIACRITICS.sub('', string)
            normalize_string = normalize_string.lower()
            normalize_string = normalize_string.strip()
        except Exception as e:
            print("Error diacritic parse {0}".format(str(e)))

        normalize_words = []
        if normalize_string:
            temp_normalize_words = re.split('\s+', normalize_string)
            for word in temp_normalize_words:
                unicode_word = self.__normalize_word(word)
                # проверка на максимальную/минимальную длину слова
                if len(unicode_word) < self.min_len_word or len(unicode_word) > self.max_len_word:
                    continue

                lang = self.__DETECTION.detect(unicode_word)
                normalize_word = unicode_word

                if lang == 1:
                    normalize_word = self.__PORTER_ST.stem(unicode_word)
                elif lang == 2:
                    normalize_word = self.__PORTER_ST.stemRu(unicode_word)

                # чтобы не добавлять пустые строки. Пример ""
                if normalize_word:
                    normalize_words.append(normalize_word)
        else:
            try:
                normalize_words = re.split('\s+', string)
            except Exception as e:
                print("Error parse {0}".format(str(e)))

        return normalize_words

    def normalize_without_repetition(self, string):
        """
        Вернуть нормализованный список слов без повторения слов.
        Это может быть нужно при поиске.

        >>> norm = Normalization()
        >>> norm.normalize_without_repetition("This testing this this")
        [u'test', u'thi']
        """
        return list(set(self.normalize(string)))

    def normalize_with_position(self, string):
        """
        Вернуть нормализированный список слов со словопозициями.

        >>> norm = Normalization()
        >>> norm.normalize_with_position("This testing this this")
        [(u'thi', 0), (u'test', 1), (u'thi', 2), (u'thi', 3)]
        """

        normalize_words = self.normalize(string)
        words_with_position = []
        iter_word = 0

        for word in normalize_words:
            words_with_position.append((word, iter_word))
            iter_word += 1

        return words_with_position