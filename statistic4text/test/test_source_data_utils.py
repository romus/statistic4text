# -*- coding: utf-8 -*-


__author__ = 'romus'

import os
import unittest
from statistic4text.utils.source_data_utils import FileSource, FileBlockSource


class TestFileSource(unittest.TestCase):

    def setUp(self):
        self.__fileSource = FileSource()
        self.__dirPath = os.path.abspath(os.curdir)

    def testGetSource(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileSource.openSource(filePath)
        self.assertIsNotNone(source, "not open source")
        self.__fileSource.closeSource(source)

    def testGetSourceThrowIOError(self):
        filePath = os.path.join(self.__dirPath, "resources/not_exist_file")
        self.assertRaises(IOError, self.__fileSource.openSource, filePath)

    def testRead(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileSource.openSource(filePath)
        for line in self.__fileSource.read(source):
            self.assertIsNotNone(line)
        self.__fileSource.closeSource(source)

    def testGetName(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileSource.openSource(filePath)
        self.assertIsNotNone(self.__fileSource.getName(source))
        self.__fileSource.closeSource(source)

    def testGetSourceSize(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileSource.openSource(filePath)
        self.assertIsNotNone(self.__fileSource.getSourceSize(source))
        self.__fileSource.closeSource(source)

    def testGetSourceDateCreated(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileSource.openSource(filePath)
        self.assertIsNotNone(self.__fileSource.getSourceDateCreated(source))
        self.__fileSource.closeSource(source)

    def testGetSourceDateModified(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileSource.openSource(filePath)
        self.assertIsNotNone(self.__fileSource.getSourceDateModified(source))
        self.__fileSource.closeSource(source)


class TestFileBlockSource(unittest.TestCase):

    def setUp(self):
        self.__fileBlockSource = FileBlockSource(blockSize=8)
        self.__dirPath = os.path.abspath(os.curdir)

    def testGetSource(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileBlockSource.openSource(filePath)
        self.assertIsNotNone(source, "not open source")
        self.__fileBlockSource.closeSource(source)

    def testGetSourceThrowIOError(self):
        filePath = os.path.join(self.__dirPath, "resources/not_exist_file")
        self.assertRaises(IOError, self.__fileBlockSource.openSource, filePath)

    def testRead(self):
        filePath = os.path.join(self.__dirPath, "resources/test_read_file")
        source = self.__fileBlockSource.openSource(filePath)
        for block in self.__fileBlockSource.read(source):
            self.assertIsNotNone(block)
        self.__fileBlockSource.closeSource(source)
