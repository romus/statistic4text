# -*- coding: utf-8 -*-

__author__ = 'romus'

import os
from abc import ABCMeta, abstractmethod, abstractproperty


FILE_SOURCE_TYPE = "file_source_type"
FILE_BLOCK_SOURCE_TYPE = "file_block_source_type"


class Source():
    """ Абстрактный класс для работы с источниками данных """

    __metaclass__ = ABCMeta

    @abstractmethod
    def openSource(self, custom):
        """
        Открыть истояник для работы

        :param custom:  объект для работы с источником
        :return:  открытый источник
        """
        return None

    @abstractmethod
    def closeSource(self, source):
        """
        Закрыть источник

        :param source:  открытый источник
        """
        pass

    @abstractmethod
    def read(self, source):
        """
        Читать данные из источника (lazy)

        :param source:  источник открытый
        :return:  прочитанные данные из источника
        """
        return None

    @abstractmethod
    def getName(self, source):
        """
        Получить имя источника в utf-8

        :param source:  источник
        :return:  имя источника
        """
        return None

    @abstractmethod
    def getSourceSize(self, source):
        """
        Получить размер данных источника в kB

        :param source:  источник
        :return:  размер данных источника
        """
        return None

    @abstractmethod
    def getSourceDateCreated(self, source):
        """
        Получить дату создания источника

        :param source:  источник
        :return:  дата создания
        """
        return None

    @abstractmethod
    def getSourceDateModified(self, source):
        """
        Получить дату последнего изменения источника

        :param source:  источник
        :return:  дата последнего изменения
        """
        return None


class SourceCustom():
    """ Настройки для работы источника """

    __metaclass__ = ABCMeta

    @abstractmethod
    def setCustom(self, custom):
        """
        Установить данные для работы с источником

        :param custom:  данные для работы с источником
        """
        pass

    @abstractmethod
    def getCustom(self):
        """
        Получить данные для работы с источником

        :return:  данные для работы с источником
        """
        return None

    custom = abstractproperty(getCustom, setCustom)


class FileSource(Source):
    """ Источник для работы с текстомыми файлами """

    def openSource(self, custom):
        """
        Открыть файл для работы

        :param custom:  полный путь к файлу
        :return:  ссылка на открытый файл
        """
        return open(custom)

    def closeSource(self, source):
        source.close()

    def read(self, source):
        """
        Читать данные из источника (lazy)

        :param source:  ссылка на открытый файл
        :raise:  если не задан источник
        """
        if not source:
            raise Exception("Source not found")

        while True:
            line = source.readline()
            if not line:
                break
            yield line

    def getName(self, source):
        """
        Получить имя файла

        :param source:  открытый файл
        :return:  полное имя файла
        """
        return os.path.abspath(source.name)

    def getSourceSize(self, source):
        """
        Получить размер файла

        :param source:  открытый файл
        :return:  размер файла в kB
        """
        return os.path.getsize(os.path.abspath(source.name)) / 1024

    def getSourceDateCreated(self, source):
        """
        Получить дату создания файла

        :param source:  открытый файл
        :return:  дата создания файла
        """
        return os.path.getctime(os.path.abspath(source.name))

    def getSourceDateModified(self, source):
        """
        Получить дату последней модификации файла

        :param source:  открытый файл
        :return:  дата последней модификации файла
        """
        return os.path.getmtime(os.path.abspath(source.name))


class FileBlockSource(FileSource):
    """ Источник для работы по блокам с текстовыми файлами """

    def __init__(self, blockSize=1024, maxSizeLastString=300, listSeparators=None):
        """
        Инициализация

        :param blockSize:  размер блока для чтения за один раз
        :param maxSizeLastString: по-умолчанию - 300
        :param listSeparators:  список с разделителями. По-умолчанию (если None) - [" ", "\n"]
        """
        self.__blockSize = blockSize
        self.__lastString = None
        self.__maxSizeLastString = maxSizeLastString
        self.__sizeLastString = 0

        if not listSeparators:
            listSeparators = [" ", "\n"]
        self.__listSeparators = listSeparators
        self.__stopIteration = False

    def read(self, source):
        self.__stopIteration = False
        self.__lastString = None
        self.__sizeLastString = 0
        while True:
            blockString = source.read(self.__blockSize)
            if not blockString and self.__lastString:
                tempLastString = self.__lastString
                self.__stopIteration = True
                yield tempLastString
            elif not blockString:
                self.__stopIteration = True

            if self.__stopIteration:
                break

            if self.__lastString:  # было непрочитанное слово из предыдущего блока
                sepIndex = self.__getFirstSeparator(blockString)
                if sepIndex != -1:  # если был найден разделитель
                    if self.__sizeLastString + sepIndex + 1 <= self.__maxSizeLastString:
                        blockString = self.__lastString + blockString
                    else:  # бывает файл в одну строку
                        blockString = blockString[sepIndex: len(blockString)]
                    self.__lastString = None
                    self.__sizeLastString = 0

            yield self.__getBlockString(blockString)

    def __getBlockString(self, blockString):
        """
        Получить обработанную строку

        :param blockString:  прочитанная из файла строка
        :return:  обработанная строка
        """
        if not blockString[-1] in self.__listSeparators:  # есть непрочитанное слово
            sepIndex = self.__getFirstSeparator(blockString, True)
            if sepIndex == -1:  # прочитанный блок и есть непрочитанное слово
                self.__lastString = self.__lastString + blockString if self.__lastString else blockString
                blockString = ""
            else:  # вырезаем непрочитанное слово
                if self.__lastString:
                    self.__lastString = self.__lastString + blockString[sepIndex: len(blockString)]
                else:
                    self.__lastString = blockString[sepIndex: len(blockString)]
                blockString = blockString[0: sepIndex]
            self.__sizeLastString = len(self.__lastString)

        return blockString

    def __getFirstSeparator(self, string, reverse=False):
        """
        Найти первое значение разделителя

        :param string:  строка
        :param reverse:  True - поиск с конца строки
        :return:  индекс найденного разделителя
        """
        findSepIndex = -1
        if string:
            for itemSep in self.__listSeparators:
                tempSepIndex = string.rfind(itemSep) if reverse else string.find(itemSep)
                if reverse:
                    findSepIndex = tempSepIndex if (tempSepIndex > findSepIndex) else findSepIndex
                else:
                    if (tempSepIndex != -1 and findSepIndex == -1) or \
                            (tempSepIndex != -1 and findSepIndex != -1 and findSepIndex < tempSepIndex):
                        findSepIndex = tempSepIndex

        return findSepIndex


class FileSourceCustom(SourceCustom):
    """ Настройки для открытия файла в ФС """

    def __init__(self):
        self.__custom = None

    def getCustom(self):
        return self.__custom

    def setCustom(self, custom):
        self.__custom = custom

    custom = property(getCustom, setCustom)


class SourceFactory():

    def createSource(self, source_type):
        """
        Создать объект для работы с источником

        :param source_type:  тип источника с данными
        """
        ret_object = None
        if source_type == FILE_SOURCE_TYPE:
            ret_object = FileSource()
        elif source_type == FILE_BLOCK_SOURCE_TYPE:
            ret_object = FileBlockSource()

        return ret_object
