# -*- coding: utf-8 -*-

__author__ = 'romus'


import sys
import datetime
from abc import ABCMeta, abstractmethod, abstractproperty
from statistic4text.errors.errors import ParamError
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.source_data_utils import Source, SourceCustom
from statistic4text.utils.normalization_utils import Normalization, DetectEncoding


MONGO_TYPE = "mongo"


class Statistic():
	""" Формирование статистики по файлам """

	__metaclass__ = ABCMeta

	@abstractmethod
	def makeDocStatistic(self, sourceName, ss, data, normalizationCallback):
		"""
		Формирование статистики по файлу

		:param sourceName:  полное имя источника (в любой кодировке)
		:param ss:  source size - размер данных источника в kB
		:param data:  данные из файла (список строк в любой кодировке)
		:param normalizationCallback:  колбэк для нормализации файла (если None, то разделение слов по пробелу)
		:rtype: NoneType
		"""
		pass

	@abstractmethod
	def makeDocStatisticCustom(self, openSourceCallback, sourceCustom, normalizationCallback):
		"""
		Формирование статистики по файлу

		:param openSourceCallback:  колбэк для получения данных из файла
		:param sourceCustom:  настройки для работы источника
		:param normalizationCallback:  колбэк для нормализации файла (если None, то разделение слов по пробелу)
		:rtype: NoneType
		"""
		pass

	@abstractmethod
	def makeTotalStatistic(self):
		"""
		Формирование статистики по всем источникам

		:rtype: NoneType
		"""
		pass

	@abstractproperty
	def getBufferSize(self):
		"""
		Получить размер буффера для хранения данных в оперативной памяти [kB]

		:return:  размер буффера в kB
		"""
		return None

	@abstractproperty
	def setBufferSize(self, bufferSize):
		""" Установить размер буффера для хранения данных в оперативной памяти [kB]"""
		pass

	@abstractmethod
	def addMoreStatistics(self, calc):
		"""
		Добавление дополнительной статистики по сохраненным словарям

		:param calc:  объект для расчета дополнительных характеристик
		"""
		pass

	bufferSize = abstractproperty(getBufferSize, setBufferSize)

	@abstractmethod
	def getMainStatisticID(self):
		"""
		Получить id сохраненного источника со статистикой

		:return:  id сохраненного источника со статистикой
		"""
		return None


class MongoStatistic(Statistic):
	""" Формирование и сохранение индекса в mongodb """

	def __init__(self, mongoUtils):
		self.__bufferSize = 2048
		self.__mongoUtils = mongoUtils
		self.__bufferDictID = None
		self.__bufferDict = {}
		self.__detectEncoding = DetectEncoding()

	def makeDocStatistic(self, sourceName, ss, data, normalizationCallback):
		if not normalizationCallback:
			raise ParamError("normalizationCallback not to be a None")

		if not isinstance(normalizationCallback, Normalization):
			raise ParamError("normalizationCallback is not instance Normalization")

		sn = self.__detectEncoding.encodeText(sourceName)
		sen = self.__detectEncoding.getEncode(sourceName)
		sde = normalizationCallback.getNormalizeTextEncode()
		sdc = datetime.datetime.now()
		normalizeData = normalizationCallback.normalizeText(data)  # нормализация полученного текста
		self.__makeDocIndex(normalizeData, True, sn, sen, ss, sde, sdc)  # сохранение
		self.__saveDict(True)  # сохранение словаря, если он что-то содержит

	def makeDocStatisticCustom(self, openSourceCallback, sourceCustom, normalizationCallback):
		if not openSourceCallback or not normalizationCallback or not sourceCustom:
			raise ParamError("openSourceCallback or normalizationCallback or sourceCustom  not to be a None")

		if not isinstance(openSourceCallback, Source):
			raise ParamError("openSourceCallback is not instance Source")

		if not isinstance(sourceCustom, SourceCustom):
			raise ParamError("sourceCustom is not instance SourceCustom")

		if not isinstance(normalizationCallback, Normalization):
			raise ParamError("normalizationCallback is not instance Normalization")

		openSource = openSourceCallback.openSource(sourceCustom.getCustom())
		isSave = True
		for itemData in openSourceCallback.read(openSource):
			try:
				normalizeData = normalizationCallback.normalizeText(itemData)  # нормализация полученного текста
				if isSave:  # добавление нового словарного индекса
					sn = self.__detectEncoding.encodeText(openSourceCallback.getName(openSource))  # имя
					sen = self.__detectEncoding.getEncode(sn)
					ss = openSourceCallback.getSourceSize(openSource)  # размер в kB
					sde = normalizationCallback.getNormalizeTextEncode()
					sdc = datetime.datetime.now()
					self.__makeDocIndex(normalizeData, isSave, sn, sen, ss, sde, sdc)  # сохранение
					isSave = False
				else:  # добавление данных к уже существующему индексу
					self.__makeDocIndex(normalizeData, isSave)
			except ParamError:
				pass
		self.__saveDict(True)  # сохранение словаря, если он что-то содержит

		openSourceCallback.closeSource(openSource)

	def makeTotalStatistic(self):
		self.__mongoUtils.mergeDicts()

	def addMoreStatistics(self, calc):
		self.__mongoUtils.addMoreStatistics(calc)

	def getBufferSize(self):
		return self.__bufferSize

	def setBufferSize(self, bufferSize):
		self.__bufferSize = bufferSize

	def getMainStatisticID(self):
		self.__mongoUtils.getMergeDictID()

	def __makeDocIndex(self, data, createNewDocIndex=False, sn=None, sen=None, ss=0, sde=None, sdc=None):
		"""
		Создание индекса по документу

		:param data:  данные для индекса
		:param createNewDocIndex:  создавать ли новый индекс по документу (True - да)
		:param sn:  source name - имя источника  (для создания индекса)
		:param sen:  sourceEncodeName - кодировка имени источника
		:param ss:  source size - размер всех данных источника
		:param sde:  source data encode - кодировка данных источника
		:param sdc:  source data created - дата создания индекса по источнику
		"""
		if createNewDocIndex:  # создание нового документа
			self.__bufferDictID = self.__mongoUtils.saveDict(sn, sen, ss, {}, sde, sdc)

		for itemWord in data:  # добавление слов в словарь
			if itemWord in self.__bufferDict:
				self.__bufferDict[itemWord] += 1
			else:
				self.__bufferDict[itemWord] = 1

			sizeDict = sys.getsizeof(self.__bufferDict, -1)
			if sizeDict == -1:
				raise TypeError("Object does not provide means to retrieve the size (see docs)")
			if sizeDict > self.getBufferSize() * 1024:
				self.__saveDict()

	def __saveDict(self, cleanDictID=False):
		"""
		Сохранение данных своваря

		:param cleanDictID:  true - удалить сключ словаря
		"""
		if self.__bufferDictID and self.__bufferDict:
			self.__mongoUtils.add2Dict(self.__bufferDictID, self.__bufferDict)
			self.__bufferDict = {}  # обновление словаря
			if cleanDictID:  # обновление ключа
				self.__bufferDictID = None

	bufferSize = property(getBufferSize, setBufferSize)


class StatisticFactory():

	def createIndex(self, indexType, saveUtil):
		"""
		Создание индексатора

		:param indexType:  тип создаваемоего объекта
		:rtype:  Statistic
		:return:  объект для создания индекса
		"""
		if not indexType:
			raise ParamError("indexType is not None or ''")

		retObject = None
		if indexType == MONGO_TYPE:
			if not isinstance(saveUtil, MongoSaveUtils):
				raise ParamError("saveUtil is not instance MongoSaveUtils")
			retObject = MongoStatistic(saveUtil)

		return retObject
