# -*- coding: utf-8 -*-


__author__ = 'romus'

from abc import ABCMeta, abstractmethod
import pymongo


class ReadUtils():

    __metaclass__ = ABCMeta

    @abstractmethod
    def getDict(self, dictID):
        """
        Получить данные по словарю по ID

        :param dictID:  ID словаря
        :rtype:  dict
        :return:  словарь с данными по словарю/файлу/источнику
        """
        return None

    @abstractmethod
    def getSubDicts(self, mergeDictID):
        """
        Получить данные по дочерним словарям (lazy)

        :param mergeDictID:  ID основного словаря
        :rtype:  dict
        :return:  словарь с данными по словарю/файлу/источнику
        """
        return None

    @abstractmethod
    def getDictData(self, dictID):
        """
        Получить данные по словарю/файлу/источнику (lazy)

        :param dictID:  ID словаря, для получения данных
        :rtype:  dict
        :return:  словарь с данными из словаря/файла/источника
        """
        return None


class MongoReadUtils(ReadUtils):

    def __init__(self, host, port, user, password, databaseName, filesCollectionName, dataFilesCollectionName):
        """
        Инициализация

        :param host:  хост
        :param port:  порт
        :param user:  пользователь
        :param password:  пароль
        :param databaseName:  имя базы
        :param filesCollectionName:  имя коллекции для описания свойств сохраняемых словарей (файлов)
        :param dataFilesCollectionName:  имя коллекции для хранения данных словарей (файлов)
        """
        self._client = pymongo.MongoClient(host=host, port=port)
        self._db = self._client[databaseName]
        self._db.authenticate(user, password)
        self._filesCollection = self._db[filesCollectionName]
        self._dataFilesCollection = self._db[dataFilesCollectionName]

    def getDict(self, dictID):
        return self._filesCollection.find_one({"_id": dictID})

    def getSubDicts(self, mergeDictID):
        return self._getLazyData(self._filesCollection, {"merge_dict_id": mergeDictID})

    def getDictData(self, dictID):
        return self._getLazyData(self._dataFilesCollection, {"dict_id": dictID})

    def _getLazyData(self, collection, findProps):
        """
        Получение данных из коллекции

        :param collection:  объект коллекции
        :param findProps:  словарь для поиска необходимых данных
        """
        while True:
            for itemData in collection.find(findProps):
                yield itemData
            break
