# -*- coding: utf-8 -*-

__author__ = 'romus'


import unittest
import datetime
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.source_data_utils import FileSource, FileBlockSource


class TestMongoSaveUtils(unittest.TestCase):

	def setUp(self):
		self.mongoUtils = None
		try:
			self.mongoUtils = MongoSaveUtils("192.168.0.80", 27017, "statistic", "statistic",
											 "statistic", "files", "files_data", "test_merge_dict")
		except:
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


class TestFileSource(unittest.TestCase):
	def setUp(self):
		self.__fileSource = FileSource()

	def testGetSource(self):
		source = self.__fileSource.openSource("resources/test_read_file")
		self.assertIsNotNone(source, "not open source")
		self.__fileSource.closeSource(source)

	def testGetSourceThrowIOError(self):
		self.assertRaises(IOError, self.__fileSource.openSource, "resources/not_exist_file")

	def testRead(self):
		source = self.__fileSource.openSource("resources/test_read_file")
		for line in self.__fileSource.read(source):
			self.assertIsNotNone(line)
		self.__fileSource.closeSource(source)


class TestFileBlockSource(unittest.TestCase):
	def setUp(self):
		self.__fileBlockSource = FileBlockSource(blockSize=8)

	def testGetSource(self):
		source = self.__fileBlockSource.openSource("resources/test_read_file")
		self.assertIsNotNone(source, "not open source")
		self.__fileBlockSource.closeSource(source)

	def testGetSourceThrowIOError(self):
		self.assertRaises(IOError, self.__fileBlockSource.openSource, "resources/not_exist_file")

	def testRead(self):
		source = self.__fileBlockSource.openSource("resources/test_read_file")
		for block in self.__fileBlockSource.read(source):
			self.assertIsNotNone(block)
		self.__fileBlockSource.closeSource(source)


if __name__ == "__main__":
	unittest.main()
