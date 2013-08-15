# -*- coding: utf-8 -*-

__author__ = 'romus'

from abc import ABCMeta, abstractmethod
import pymongo


class SaveUtils():
	""" Сохранение индексных данных """

	__metaclass__ = ABCMeta

	@abstractmethod
	def saveDict(self, dictName, dictNameEncode, data, dataEncode, dateIndex):
		"""
		Сохранить словарь с данными

		:param dictName:  имя словаря (utf-8)
		:param dictNameEncode:  кодировка имени словаря
		:param data:  данные. Пример, {слово: частота_слова_в_словаре, ...} (utf-8)
		:param dataEncode:  кодировка данных словаря
		:param dateIndex: дата создания индекса по словарю
		:return:  id сохраненного словаря
		"""
		return -1

	@abstractmethod
	def add2Dict(self, dictID, data):
		"""
		Добавление данных к уже существующему словарю, если словарь не сохранен,
		то создается новый словарь.

		:param dictID:  имя сохраненного словаря
		:param data:  данные. Пример, {слово: частота_слова_в_словаре, ...}
		"""
		pass

	@abstractmethod
	def mergeDicts(self):
		""" Слияние всех словарей, которые до этого были сохранены """
		pass


class MongoSaveUtils(SaveUtils):
	""" Сохранение индексных данных в mongodb """

	INDEX_FIELDS_FILES_COLLECTION = []
	INDEX_FIELDS_DATA_FILES_COLLECTION = [("word", pymongo.DESCENDING), ("dict_id", pymongo.DESCENDING)]

	def __init__(self, host, port, user, password, databaseName, filesCollectionName, dataFilesCollectionName):
		"""
		Инициализация

		:param host:  хост
		:param port:  порт
		:param user:  пользователь
		:param password:  пароль
		"""
		self.__client = pymongo.MongoClient(host=host, port=port)
		self.__db = self.__client[databaseName]
		self.__db.authenticate(user, password)
		self.__filesCollection = self.__db[filesCollectionName]
		self.__dataFilesCollection = self.__db[dataFilesCollectionName]
		self.__filesCollection.remove()
		self.__dataFilesCollection.remove()

		# создание индекса для коллекций файлов и данных по файлам
		if len(self.INDEX_FIELDS_FILES_COLLECTION) > 0:
			self.__filesCollection.create_index(self.INDEX_FIELDS_FILES_COLLECTION)
		if len(self.INDEX_FIELDS_DATA_FILES_COLLECTION) > 0:
			self.__dataFilesCollection.create_index(self.INDEX_FIELDS_DATA_FILES_COLLECTION)

	def saveDict(self, dictName, dictNameEncode, data, dataEncode, dateIndex):
		dictID = self.__filesCollection.insert({"dict_name": dictName, "dict_name_encode": dictNameEncode,
												"data_encode": dataEncode, "dict_type": 1,
												"date_index": dateIndex})
		for key, value in data.iteritems():
			self.__dataFilesCollection.insert({"word": key, "df": value, "dict_id": dictID})

		return dictID

	def add2Dict(self, dictID, data):
		for key, value in data.iteritems():
			pass
			word = self.__dataFilesCollection.find_one({"dict_id": dictID, "word": key})
			if word:  # обновляем документальную частоту
				self.__dataFilesCollection.update({"_id": word['_id']}, {"$set": {"df": word['df'] + value}})
			else:  # вставляем новую запись
				self.__dataFilesCollection.insert({"word": key, "df": value, "dict_id": dictID})

	def mergeDicts(self):
		pass
