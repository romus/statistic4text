# -*- coding: utf-8 -*-


__author__ = 'romus'


import os
import unittest
from statistic4text.calc.calc import CalcMongo
from statistic4text.errors.errors import DataNotFound
from statistic4text.utils.save_utils import MongoSaveUtils
from statistic4text.statistic.statistic import MongoStatistic
from statistic4text.utils.normalization_utils import SimpleNormalization
from statistic4text.utils.source_data_utils import FileBlockSource, FileSourceCustom


class TestMongoStatistic(unittest.TestCase):

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
		self.__calcMongo = CalcMongo()
		self.__mongoStatistics = MongoStatistic(self.__mongoUtils)
		self.__dirPath = os.path.abspath(os.curdir)

	def tearDown(self):
		try:
			self.__mongoUtils.deleteMergeDict()
		except DataNotFound:
			pass

	def testMakeDocStatisticCustomUtf8(self):
		filePath = os.path.join(self.__dirPath, "resources/test_mongo_index_utf8")
		self.__fileSourceCustom.custom = filePath
		self.__mongoStatistics.makeDocStatisticCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoStatistics.makeTotalStatistic()

	def testMakeDocStatisticCustomWin1251(self):
		filePath = os.path.join(self.__dirPath, "resources/test_mongo_index_win1251")
		self.__fileSourceCustom.custom = filePath
		self.__mongoStatistics.makeDocStatisticCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoStatistics.makeTotalStatistic()

	def testMakeDocStatisticCustomWin866(self):
		filePath = os.path.join(self.__dirPath, "resources/test_mongo_index_win866")
		self.__fileSourceCustom.custom = filePath
		self.__mongoStatistics.makeDocStatisticCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoStatistics.makeTotalStatistic()

	def testMakeDocStatistic(self):
		data = "Проверка проверка сохранения индекса. Check save statistic"
		self.__mongoStatistics.makeDocStatistic("test_source_name", 1234, data, self.__simpleNormal)
		self.__mongoStatistics.makeTotalStatistic()

	def testAddMoreStatistics(self):
		filePath = os.path.join(self.__dirPath, "resources/test_mongo_index_utf8")
		self.__fileSourceCustom.custom = filePath
		self.__mongoStatistics.makeDocStatisticCustom(self.__fileBlockSource, self.__fileSourceCustom, self.__simpleNormal)
		self.__mongoStatistics.makeTotalStatistic()
		self.__mongoUtils.addMoreStatistics(self.__calcMongo)
