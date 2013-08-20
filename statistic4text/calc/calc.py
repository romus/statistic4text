# -*- coding: utf-8 -*-


__author__ = 'romus'


import math
from abc import ABCMeta, abstractmethod
from statistic4text.errors.errors import ParamError


class Calc():

	__metaclass__ = ABCMeta

	@abstractmethod
	def calcIDF(self, *args):
		"""
		Вычислить обратную документальную частоту для термина в коллекции

		:param args:  необходимые параметры
		:rtype:  float
		:return:  обратная документальная частота термина в коллекции (idf)
		"""
		return None

	@abstractmethod
	def calcTF_IDF(self, *args):
		"""
		Вычислить комбинированное значение частоты и обратной документальной частоты термина

		:param args:  необходимые параметры
		:rtype: float
		:return:  значение частоты и обратной документальной частоты термина
		"""
		return None


class CalcMongo(Calc):

	def calcIDF(self, *args):
		"""
		Вычислить обратную документальную частоту для термина в коллекции

		:param args:  (частота_термина_в_коллекции, количество_документов_в_коллекции)
		:rtype:  float
		:return:  обратная документальная частота термина в коллекции (idf)
		"""
		if not args or len(args) < 2:
			raise ParamError("Must to be 2 args")

		idf = 0

		try:
			idf = math.log10(args[1] / args[0])
		except ValueError:
			pass
		return idf

	def calcTF_IDF(self, *args):
		"""
		Вычислить комбинированное значение частоты и обратной документальной частоты термина

		:param args:  (частота_термина_в_документе, обратная_документальная_частота_термина_в_коллекции)
		:rtype: float
		:return:  значение частоты и обратной документальной частоты термина
		"""
		if not args or len(args) < 2:
			raise ParamError("Must to be 2 args")

		return args[0] * args[1]
