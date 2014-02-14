# -*- coding: utf-8 -*-


__author__ = 'romus'

import os
import unittest
from statistic4text.errors.errors import ParamError
from statistic4text.utils.normalization_utils import DetectEncoding, SimpleNormalization


class TestDetectEncoding(unittest.TestCase):

    def setUp(self):
        self.__detectEncoding = DetectEncoding()
        self.__dirPath = os.path.abspath(os.curdir)

    def testGetEncode(self):
        filePath = os.path.join(self.__dirPath, "resources/test_encode_utf8")
        with open(filePath) as utf8File:
            utf8Encode = self.__detectEncoding.getEncode(utf8File.read())
            self.assertEqual(utf8Encode, "utf-8", "fail detect encode test_encode_utf8")

        filePath = os.path.join(self.__dirPath, "resources/test_encode_win1251")
        with open(filePath) as win1251File:
            win1251Encode = self.__detectEncoding.getEncode(win1251File.read())
            self.assertEqual(win1251Encode, "windows-1251", "fail detect encode test_encode_win1251")

        filePath = os.path.join(self.__dirPath, "resources/test_encode_win866")
        with open(filePath) as win866File:
            win866Encode = self.__detectEncoding.getEncode(win866File.read())
            self.assertEqual(win866Encode, "IBM866", "fail detect encode test_encode_win866")

    def testGetEncode1TypeError(self):
        self.assertRaises(TypeError, self.__detectEncoding.getEncode, 123)
        self.assertRaises(TypeError, self.__detectEncoding.getEncode, None)

    def testEncode(self):
        filePath = os.path.join(self.__dirPath, "resources/test_encode_win1251")
        with open(filePath) as win1251File:
            utf8Text = self.__detectEncoding.encodeText(win1251File.read(), "utf-8")
            utf8Encode = self.__detectEncoding.getEncode(utf8Text)
            self.assertEqual(utf8Encode, "utf-8", "fail encode text from test_encode_win1251")

    def testEncodeLookupError(self):
        filePath = os.path.join(self.__dirPath, "resources/test_encode_win1251")
        with open(filePath) as win1251File:
            self.assertRaises(LookupError, self.__detectEncoding.encodeText, win1251File.read(), "utf-8_test_")


class TestSimpleNormalization(unittest.TestCase):

    def setUp(self):
        self.__simpleNormalization = SimpleNormalization()
        self.__dirPath = os.path.abspath(os.curdir)
        self.__normalizeWords = ["thi", "test", "file", "encod", "проверк", "определен", "кодировк", "фа"]

    def testNormalizeText(self):
        filePath = os.path.join(self.__dirPath, "resources/test_encode_utf8")
        with open(filePath) as utf8File:
            words = self.__simpleNormalization.normalizeText(utf8File.read())
            for itemWord in words:
                self.assertIn(itemWord, self.__normalizeWords, "not normalized test_encode_utf8")

        filePath = os.path.join(self.__dirPath, "resources/test_encode_win1251")
        with open(filePath) as win1251File:
            words = self.__simpleNormalization.normalizeText(win1251File.read())
            for itemWord in words:
                self.assertIn(itemWord, self.__normalizeWords, "not normalized test_encode_win1251")

        filePath = os.path.join(self.__dirPath, "resources/test_encode_win866")
        with open(filePath) as win866File:
            words = self.__simpleNormalization.normalizeText(win866File.read())
            for itemWord in words:
                self.assertIn(itemWord, self.__normalizeWords, "not normalized test_encode_win866")

    def testNormalizeTextParamError(self):
        self.assertRaises(ParamError, self.__simpleNormalization.normalizeText, None)
        self.assertRaises(ParamError, self.__simpleNormalization.normalizeText, "")

