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
		return  None


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
		self.__client = pymongo.MongoClient(host=host, port=port)
		self.__db = self.__client[databaseName]
		self.__db.authenticate(user, password)
		self.__filesCollection = self.__db[filesCollectionName]
		self.__dataFilesCollection = self.__db[dataFilesCollectionName]

	def getDict(self, dictID):
		return self.__filesCollection.find_one({"_id": dictID})

	def getSubDicts(self, mergeDictID):
		return self.__getLazyData(self.__filesCollection, {"merge_dict_id": mergeDictID})

	def getDictData(self, dictID):
		return self.__getLazyData(self.__dataFilesCollection, {"dict_id": dictID})

	def __getLazyData(self, collection, findProps):
		"""
		Получение данных из коллекции

		:param collection:  объект коллекции
		:param findProps:  словарь для поиска необходимых данных
		"""
		while True:
			for itemData in collection.find(findProps):
				yield itemData
			break
