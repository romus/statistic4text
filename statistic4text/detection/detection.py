# -*- coding: utf-8 -*-

__author__ = 'romus'

ABC_RUS = [1040, 1103, [1025, 1105]]
ABC_ENG = [65, 122]


class Detection(object):
    def __init__(self):
        super(Detection, self).__init__()

    def __checkSymbol(self, abc, symbol):
        extSymbol = None if len(abc) == 2 else abc[2]

        if extSymbol:
            retVal = abc[0] <= symbol <= abc[1] or symbol in extSymbol
        else:
            retVal = abc[0] <= symbol <= abc[1]

        return retVal

    def check_symbol(self, sym, abc_rus=ABC_RUS, abc_eng=ABC_ENG):
        """
        Проверка символа на принадлежность алфавиту

        :param sym: символ, например "а"
        :param abc_rus: русский алфавит
        :param abc_eng: английский алфавит
        :return: try - принадлежит, false - непринадлежит
        """

        return self.__checkSymbol(abc_rus, ord(sym)) or self.__checkSymbol(abc_eng, ord(sym))

    def detect(self, word, abc_rus=ABC_RUS, abc_eng=ABC_ENG):
        """
        Определить язык

        >>> test_det = Detection()
        >>> test_det.detect("test")
        1
        >>> test_det.detect("t.e.s.t")
        0
        >>> # test_det.detect(u"проверка") -> 2 только для unicode
        """

        lang = 0
        checkABC = None

        try:    # может быть задана пустая строка
            if self.__checkSymbol(abc_eng, ord(word[0])):
                checkABC = abc_eng
                lang = 1
            elif self.__checkSymbol(abc_rus, ord(word[0])):
                checkABC = abc_rus
                lang = 2
        except IndexError:
            pass

        if not checkABC:
            return 0

        for i in range(1, len(word)):
            if not self.__checkSymbol(checkABC, ord(word[i])):
                return 0

        return lang
