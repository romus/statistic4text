# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
from statistic4text.utils.normalization_utils import DetectEncoding


class TestDetectEncoding(unittest.TestCase):

	def setUp(self):
		self.__detectEncoding = DetectEncoding()

	def testGetEncode(self):
		with open("resources/test_encode_utf8") as utf8File:
			utf8Encode = self.__detectEncoding.getEncode(utf8File.read())
			self.assertEqual(utf8Encode, "utf-8", "fail detect encode test_encode_utf8")

		with open("resources/test_encode_win1251") as win1251File:
			win1251Encode = self.__detectEncoding.getEncode(win1251File.read())
			self.assertEqual(win1251Encode, "windows-1251", "fail detect encode test_encode_win1251")

		with open("resources/test_encode_win866") as win866File:
			win866Encode = self.__detectEncoding.getEncode(win866File.read())
			self.assertEqual(win866Encode, "IBM866", "fail detect encode test_encode_win866")

	def testGetEncode1TypeError(self):
		self.assertRaises(TypeError, self.__detectEncoding.getEncode, 123)
		self.assertRaises(TypeError, self.__detectEncoding.getEncode, None)

	def testEncode(self):
		with open("resources/test_encode_win1251") as win1251File:
			utf8Text = self.__detectEncoding.encodeText(win1251File.read(), "utf-8")
			utf8Encode = self.__detectEncoding.getEncode(utf8Text)
			self.assertEqual(utf8Encode, "utf-8", "fail encode text from test_encode_utf8")

	def testEncodeLookupError(self):
		with open("resources/test_encode_win1251") as win1251File:
			self.assertRaises(LookupError, self.__detectEncoding.encodeText, win1251File.read(), "utf-8_test_")


if __name__ == "__main__":
	unittest.main()
