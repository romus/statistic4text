# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
from statistic4text.utils.source_data_utils import FileSource, FileBlockSource


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