# -*- coding: utf-8 -*-

__author__ = 'romus'

from abc import ABCMeta, abstractmethod, abstractproperty


class Index():
	""" Формирование статистики по файлам """

	__metaclass__ = ABCMeta

	@abstractmethod
	def makeDocIndex(self, sourceName, data, normalizationCallback=None):
		"""
		Формирование индекса по файлу

		:param sourceName:  полное имя источника (в любой кодировке)
		:param data:  данные из файла (список строк в любой кодировке)
		:param normalizationCallback:  колбэк для нормализации файла (если None, то разделение слов по пробелу)
		"""
		pass

	@abstractmethod
	def makeDocIndex(self, fileName, openFileCallback, normalizationCallback=None):
		"""
		Формирование индекса по файлу

		:param fileName: полное имя файла (в любой кодировке)
		:param openFileCallback:  колбэк для получения данных из файла
		:param normalizationCallback:  колбэк для нормализации файла (если None, то разделение слов по пробелу)
		"""
		pass

	@abstractmethod
	def makeTotalIndex(self):
		""" Формирование общего индекса по всем файлам """
		pass

	@abstractproperty
	def getBufferSize(self):
		""" Получить размер буффера для хранения данных в оперативной памяти [kB]"""
		pass

	@abstractproperty
	def setBufferSize(self, bufferSize):
		""" Установить размер буффера для хранения данных в оперативной памяти [kB]"""
		pass

	bufferSize = abstractproperty(getBufferSize, setBufferSize)
