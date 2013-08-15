# -*- coding: utf-8 -*-

__author__ = 'romus'

from index import Index


class MongoIndex(Index):
	""" Формирование и сохранение индекса в mongodb """

	def __init__(self, mongoUtils):
		self.__bufferSize = 2048
		self.__mongoUtils = mongoUtils

	def makeDocIndex(self, sourceName, data, normalizationCallback=None):
		pass

	def makeDocIndex(self, fileName, openFileCallback, normalizationCallback=None):
		pass

	def makeTotalIndex(self):
		super(MongoIndex, self).makeTotalIndex()

	def getBufferSize(self):
		return self.__bufferSize

	def setBufferSize(self, bufferSize):
		self.__bufferSize = bufferSize

	bufferSize = property(getBufferSize, setBufferSize)
