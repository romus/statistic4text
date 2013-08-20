# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
from statistic4text.calc.calc import CalcMongo
from  statistic4text.errors.errors import ParamError


class TestCalcMongo(unittest.TestCase):

	def setUp(self):
		self.__calcMongo = CalcMongo()

	def testCalcIDF(self):
		self.assertEqual(self.__calcMongo.calcIDF(1, 1), 0, "lg(1) != 0")
		self.assertEqual(self.__calcMongo.calcIDF(10, 100), 1, "lg(10) != 1")
		self.assertEqual(self.__calcMongo.calcIDF(100, 2), 0, "idf != 0")

	def testCalcIDFException(self):
		self.assertRaises(ParamError, self.__calcMongo.calcIDF)
		self.assertRaises(ParamError, self.__calcMongo.calcIDF, 10)
		self.assertRaises(TypeError, self.__calcMongo.calcIDF, 10, 'sf')

	def testCalcTF_IDF(self):
		self.assertEqual(self.__calcMongo.calcTF_IDF(10, 10), 100, "10 * 10 != 100")

	def testCalcTF_IDFException(self):
		self.assertRaises(ParamError, self.__calcMongo.calcTF_IDF)
		self.assertRaises(ParamError, self.__calcMongo.calcTF_IDF, 10)


# if __name__ == "__main__":
# 	unittest.main()
