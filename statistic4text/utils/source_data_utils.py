# -*- coding: utf-8 -*-

__author__ = 'romus'


from abc import ABCMeta, abstractmethod


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
		try:
			source.close()
		except Exception as e:
			pass

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
