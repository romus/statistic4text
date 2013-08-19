# -*- coding: utf-8 -*-


__author__ = 'romus'


import unittest
from statistic4text.index.index import MongoIndex
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.utils.normalization_utils import SimpleNormalization
from statistic4text.utils.source_data_utils import FileBlockSource, FileSourceCustom


class TestMongoIndex(unittest.TestCase):

	def setUp(self):
		h = "192.168.0.80"
		p = 27017
		usr = "statistic"
		pwd = "statistic"
		db = "statistic"
		fc_n = "files"
		fc_dn = "files_data"
		mdn = "test_merge_dict"
		self.__mongoUtils = MongoSaveUtils(h, p, usr, pwd, db, fc_n, fc_dn, mdn)
		self.__simpleNormal = SimpleNormalization()
		self.__fileSourceCustom = FileSourceCustom()
		self.__fileBlockSource = FileBlockSource()
		self.__mongoIndex = MongoIndex(self.__mongoUtils)

	def testMakeDocIndexCustomUtf8(self):
		self.__fileSourceCustom.custom = "resources/test_mongo_index_utf8"
		self.__mongoIndex.makeDocIndexCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoIndex.makeTotalIndex()

	def testMakeDocIndexCustomWin1251(self):
		self.__fileSourceCustom.custom = "resources/test_mongo_index_win1251"
		self.__mongoIndex.makeDocIndexCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoIndex.makeTotalIndex()

	def testMakeDocIndexCustomWin866(self):
		self.__fileSourceCustom.custom = "resources/test_mongo_index_win866"
		self.__mongoIndex.makeDocIndexCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoIndex.makeTotalIndex()

	def testMakeDocIndex(self):
		data = "Проверка проверка сохранения индекса. Check save index"
		self.__mongoIndex.makeDocIndex("test_source_name", 1234, data, self.__simpleNormal)
		self.__mongoIndex.makeTotalIndex()

if __name__ == "__main__":
	unittest.main()
