# -*- coding: utf-8 -*-

__author__ = 'romus'


import unittest
import datetime
from pymongo.errors import ConnectionFailure
from statistic4text.utils.save_utils import MongoSaveUtils


class TestMongoSaveUtils(unittest.TestCase):

	def setUp(self):
		self.mongoUtils = None
		h = "192.168.0.80"
		p = 27017
		usr = "statistic"
		pwd = "statistic"
		db = "statistic"
		fc_n = "files"
		fc_dn = "files_data"
		mdn = "test_merge_dict"
		try:
			self.mongoUtils = MongoSaveUtils(h, p, usr, pwd, db, fc_n, fc_dn, mdn)
		except ConnectionFailure as e:
			pass

	def testConnection(self):
		self.assertIsNotNone(self.mongoUtils, "connection is fail")

	def testSaveAddDict(self):
		self.testConnection()
		insertID = self.mongoUtils.saveDict("test_dict", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.mongoUtils.add2Dict(insertID, {"plus": 1, "test": 2})
		self.mongoUtils.deleteMergeDict()

	def testMergeDicts(self):
		self.testConnection()
		self.assertIsNotNone(self.mongoUtils, "connection is ok")
		insertID = self.mongoUtils.saveDict("test_dict", "utf-8", 1234, {"the": 1, "test": 2},
											"utf-8", datetime.datetime.now())
		self.assertIsNotNone(insertID)

		insertID = self.mongoUtils.saveDict("test_dict2", "utf-8", 4321, {"the": 100, "object": 2},
											'utf-8', datetime.datetime.now())
		self.assertIsNotNone(insertID)
		self.mongoUtils.mergeDicts()


if __name__ == "__main__":
	unittest.main()
