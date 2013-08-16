# -*- coding: utf-8 -*-

__author__ = 'romus'


import unittest
import datetime
from statistic4text.utils.save_utils import MongoSaveUtils


class TestMongoSaveUtils(unittest.TestCase):

	def setUp(self):
		self.mongoUtils = MongoSaveUtils("192.168.0.80", 27017, "statistic", "statistic",
										 "statistic", "files", "files_data", "test_merge_dict")

	def testSaveAddDict(self):
		insertID = self.mongoUtils.saveDict("test_dict", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.mongoUtils.add2Dict(insertID, {"plus": 1, "test": 2})
		self.mongoUtils.deleteMergeDict()

	def testMergeDicts(self):
		insertID = self.mongoUtils.saveDict("test_dict", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)

		insertID = self.mongoUtils.saveDict("test_dict2", "utf-8", 4321, {"the": 100, "object": 2},
								 "utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.mongoUtils.mergeDicts()


if __name__ == "__main__":
	unittest.main()