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
			raise  Exception("Source not found")

		while True:
			line = source.readline()
			if not line:
				break
			yield line
