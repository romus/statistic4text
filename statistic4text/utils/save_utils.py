# -*- coding: utf-8 -*-

__author__ = 'romus'

import datetime
from abc import ABCMeta, abstractmethod
import pymongo
from statistic4text.calc.calc import CalcMongo
from statistic4text.errors.errors import ParamError, DataNotFound


class SaveUtils():
	""" Сохранение индексных данных """

	__metaclass__ = ABCMeta

	@abstractmethod
	def saveDict(self, dictName, dictNameEncode, dictSize, data, dataEncode, dateIndex):
		"""
		Сохранить словарь с данными

		:param dictName:  имя словаря (utf-8)
		:param dictNameEncode:  кодировка имени словаря
		:param dictSize:  размер словаря (файла) в kB
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
		"""
		Слияние всех словарей, которые до этого были сохранены

		:return:  id результирующего словаря
		"""
		return -1

	@abstractmethod
	def deleteMergeDict(self):
		""" Удалить итоговой словарь """
		pass

	@abstractmethod
	def deleteDicts(self):
		""" Удалить все созданные данные по словарям (файлам) """
		pass

	@abstractmethod
	def getMergeDictID(self):
		""" Получить id итогового словаря """
		return -1

	@abstractmethod
	def addMoreStatistics(self, calc):
		"""
		Добавление дополнительной статистики по сохраненным словарям

		:param calc:  объект для расчета дополнительных характеристик
		"""
		pass


class MongoSaveUtils(SaveUtils):
	""" Сохранение индексных данных в mongodb """

	INDEX_FIELDS_FILES_COLLECTION = [("dict_type", pymongo.DESCENDING)]
	INDEX_FIELDS_DATA_FILES_COLLECTION = [("word", pymongo.DESCENDING), ("dict_id", pymongo.DESCENDING)]

	def __init__(self, host, port, user, password, databaseName, filesCollectionName, dataFilesCollectionName,
				 mergeDictName="merge_dict", isDeleteAll=False):
		"""
		Инициализация

		:param host:  хост
		:param port:  порт
		:param user:  пользователь
		:param password:  пароль
		:param databaseName:  имя базы
		:param filesCollectionName:  имя коллекции для описания свойств сохраняемых словарей (файлов)
		:param dataFilesCollectionName:  имя коллекции для хранения данных словарей (файлов)
		:param mergeDictName:  имя словаря (по-умолчанию - "merge_dict") для наименования слияния словарей
		:param isDeleteAll:  удалять все старые данные из коллекций (по-умолчанию - false)
		"""
		self.__client = pymongo.MongoClient(host=host, port=port)
		self.__db = self.__client[databaseName]
		self.__db.authenticate(user, password)
		self.__filesCollection = self.__db[filesCollectionName]
		self.__dataFilesCollection = self.__db[dataFilesCollectionName]

		if isDeleteAll:  # если необходимо удалить старые данные
			self.__filesCollection.remove()
			self.__dataFilesCollection.remove()

		# сразу создаётся итоговый словарь
		self.__mergeDictID = self.__filesCollection.insert({"dict_name": mergeDictName, "dict_type": 2,
															"date_index": datetime.datetime.now()})

		# создание индекса для коллекций файлов и данных по файлам
		if len(self.INDEX_FIELDS_FILES_COLLECTION) > 0:
			self.__filesCollection.create_index(self.INDEX_FIELDS_FILES_COLLECTION)
		if len(self.INDEX_FIELDS_DATA_FILES_COLLECTION) > 0:
			self.__dataFilesCollection.create_index(self.INDEX_FIELDS_DATA_FILES_COLLECTION)

	def saveDict(self, dictName, dictNameEncode, dictSize, data, dataEncode, dateIndex):
		self.__checkExistMergeDict()

		dictID = self.__filesCollection.insert({"dict_name": dictName, "dict_name_encode": dictNameEncode,
												"dict_size": dictSize, "data_encode": dataEncode,
												"dict_type": 1, "date_index": dateIndex,
												"merge_dict_id": self.__mergeDictID})
		for key, value in data.iteritems():
			self.__dataFilesCollection.insert({"word": key, "tf": value, "dict_id": dictID})

		return dictID

	def add2Dict(self, dictID, data):
		self.__checkExistMergeDict()

		checkFile = self.__filesCollection.find_one({"_id": dictID})
		if not checkFile:  # если файла в коллекции файлов нет
			return

		for key, value in data.iteritems():
			word = self.__dataFilesCollection.find_one({"dict_id": dictID, "word": key})
			if word:  # обновляем частоту терминов в документе (term frequency - tf)
				self.__dataFilesCollection.update({"_id": word['_id']}, {"$set": {"tf": word['tf'] + value}})
			else:  # вставляем новую запись
				self.__dataFilesCollection.insert({"word": key, "tf": value, "dict_id": dictID})

	def mergeDicts(self):
		self.__checkExistMergeDict()

		# найдем все файлы, по которым раннее строился индекс
		files = self.__filesCollection.find({"dict_type": 1, "merge_dict_id": self.__mergeDictID}, fields=["_id"])
		for itemFile in files:
			# найдем все данные по словарю (файлу)
			words = self.__dataFilesCollection.find({"dict_id": itemFile["_id"]}, fields=["word", "tf"])
			for itemWord in words:
				# найти слово в итоговом словаре
				mergeWord = self.__dataFilesCollection.find_one(
					{"dict_id": self.__mergeDictID, "word": itemWord['word']})
				if mergeWord:  # обновление существующей записи
					self.__dataFilesCollection.update({"_id": mergeWord['_id']},
													  {"$set": {"cf": mergeWord['cf'] + itemWord['tf'],
																"df": mergeWord['df'] + 1}})
				else:  # добавление новой записи
					self.__dataFilesCollection.insert({"dict_id": self.__mergeDictID, "word": itemWord['word'],
													   "cf": itemWord['tf'], "df": 1})

		return self.__mergeDictID

	def deleteMergeDict(self):
		self.__checkExistMergeDict()

		self.deleteDicts()
		self.__filesCollection.remove({"_id": self.__mergeDictID})
		self.__dataFilesCollection.remove({"dict_id": self.__mergeDictID})
		self.__mergeDictID = None

	def deleteDicts(self):
		self.__checkExistMergeDict()

		files = self.__filesCollection.find({"merge_dict_id": self.__mergeDictID}, fields=["_id"])
		if files:
			for itemFile in files:  # удаление всех данных из созданных словарей
				self.__dataFilesCollection.remove({"dict_id": itemFile["_id"]})

		# удаление самих словарей (файлов)
		self.__filesCollection.remove({"merge_dict_id": self.__mergeDictID})

	def getMergeDictID(self):
		return self.__mergeDictID

	def addMoreStatistics(self, calc):
		if not calc:
			raise ParamError("calc not to be a None")
		if not isinstance(calc, CalcMongo):
			raise ParamError("calc is not instance CalcMongo")
		self.__checkExistMergeDict()

		# расчет обратной документальной частоты
		dicts = self.__filesCollection.find({"merge_dict_id": self.__mergeDictID}, fields=["_id"])
		countDicts = dicts.count()  # количество файлов
		docsDataMergeDict = self.__dataFilesCollection.find({"dict_id": self.__mergeDictID}, fields=["_id", "cf"])
		for itemDataMergeDict in docsDataMergeDict:
			updateIDF = calc.calcIDF(itemDataMergeDict["cf"], countDicts)
			self.__dataFilesCollection.update({"_id": itemDataMergeDict["_id"]}, {"$set": {"idf": updateIDF}})

		# расчет комбинированного значения частоты и обратной документальной частоты термина
		for itemDict in dicts:
			# получить все данные по словарю
			dataDict = self.__dataFilesCollection.find({"dict_id": itemDict["_id"]}, fields=["_id", "tf", "word"])
			for itemData in dataDict:
				# получить idf по слову
				dataIDF = self.__dataFilesCollection.find_one({"dict_id": self.__mergeDictID, "word": itemData["word"]},
															  fields=["idf"])
				updateTF_IDF = calc.calcTF_IDF(itemData["tf"], dataIDF["idf"])
				self.__dataFilesCollection.update({"_id": itemData["_id"]}, {"$set": {"tf_idf": updateTF_IDF}})

	def __checkExistMergeDict(self):
		""" Проверка на существование итогового словаря. Если словаря нет, то выбрасывается исключение. """

		if not self.__mergeDictID:  # если нет документа итогового словаря
			raise DataNotFound("All created data was removed (was invoked deleteMergeDict() method)")
