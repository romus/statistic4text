# -*- coding: utf-8 -*-

__author__ = 'romus'


import unittest
import datetime
from pymongo.errors import ConnectionFailure
from statistic4text.calc.calc import CalcMongo
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.errors.errors import ParamError, DataNotFound


class TestMongoSaveUtils(unittest.TestCase):

	def setUp(self):
		self.__mongoUtils = None
		h = "192.168.0.80"
		p = 27017
		usr = "statistic"
		pwd = "statistic"
		db = "statistic"
		fc_n = "files"
		fc_dn = "files_data"
		mdn = "test_merge_dict"
		try:
			self.__mongoUtils = MongoSaveUtils(h, p, usr, pwd, db, fc_n, fc_dn, mdn)
			self.calcMongo = CalcMongo()
		except ConnectionFailure as e:
			pass

	def tearDown(self):
		try:
			self.__mongoUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testConnection(self):
		self.assertIsNotNone(self.__mongoUtils, "connection is fail")

	def testGetMergeDictID(self):
		self.assertIsNotNone(self.__mongoUtils.getMergeDictID(), "fail to get merge dict ID")

	def testSaveAddDict(self):
		insertID = self.__mongoUtils.saveDict("test_dict", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.__mongoUtils.add2Dict(insertID, {"plus": 1, "test": 2})
		self.__mongoUtils.deleteMergeDict()

	def testMergeDicts(self):
		self.assertIsNotNone(self.__mongoUtils, "connection is ok")
		insertID = self.__mongoUtils.saveDict("test_dict1", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)

		insertID = self.__mongoUtils.saveDict("test_dict2", "utf-8", 4321, {"the": 100, "object": 2},
											'utf-8', datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.__mongoUtils.mergeDicts()

	def testAddMoreStatistics(self):
		self.assertIsNotNone(self.__mongoUtils, "connection is ok")
		insertID = self.__mongoUtils.saveDict("test_dict3", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)

		insertID = self.__mongoUtils.saveDict("test_dict4", "utf-8", 4321, {"the": 100, "object": 1},
											'utf-8', datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.__mongoUtils.mergeDicts()
		self.__mongoUtils.addMoreStatistics(self.calcMongo)

	def testAddMoreStatisticsException(self):
		self.assertRaises(ParamError, self.__mongoUtils.addMoreStatistics, None)
		self.assertRaises(ParamError, self.__mongoUtils.addMoreStatistics, 1234)
		self.__mongoUtils.deleteMergeDict()
		self.assertRaises(DataNotFound, self.__mongoUtils.addMoreStatistics, self.calcMongo)

