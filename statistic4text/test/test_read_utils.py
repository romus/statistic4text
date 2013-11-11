# -*- coding: utf-8 -*-


__author__ = 'romus'


import datetime
import unittest

from statistic4text.test.connection_configs import *
from statistic4text.utils.read_utils import MongoReadUtils
from statistic4text.utils.save_utils import MongoSaveUtils


class TestMongoReadUtils(unittest.TestCase):

	def setUp(self):
		date_now = datetime.datetime.now()
		self.__mongoReadUtils = MongoReadUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN)
		self.__mongoUtils = MongoSaveUtils(HOST, PORT, USR, PWD, DB, FC_N, FC_DN, MDN)
		self.__mongoUtils.saveDict("test_dict1", "utf-8", 1234, {"the": 1, "test": 2}, "utf-8", date_now)
		self.__mongoUtils.saveDict("test_dict2", "utf-8", 4321, {"the": 100, "object": 2}, 'utf-8', date_now)
		self.__mongoUtils.mergeDicts()

	def tearDown(self):
		self.__mongoUtils.deleteMergeDict()

	def testGetDict(self):
		self.assertIsNotNone(self.__mongoReadUtils.getDict(self.__mongoUtils.getMergeDictID()), "dict not found")

	def testGetSubDicts(self):
		for itemSubDicts in self.__mongoReadUtils.getSubDicts(self.__mongoUtils.getMergeDictID()):
			self.assertIsNotNone(itemSubDicts, "sub dict get exception")

	def testGetDictData(self):
		for itemDictData in self.__mongoReadUtils.getDictData(self.__mongoUtils.getMergeDictID()):
			self.assertIsNotNone(itemDictData, "dict data is not found")
