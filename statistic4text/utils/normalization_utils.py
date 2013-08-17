# -*- coding: utf-8 -*-


__author__ = 'romus'

import re
import unicodedata
import chardet
from abc import ABCMeta, abstractmethod, abstractproperty
from statistic4text.errors.errors import ParamError
from statistic4text.detection.detection import Detection
from statistic4text.stemming.porter_stemmer import PorterStemming


class DetectEncoding():
	""" Класс для определения кодировки текста """

	def getEncode(self, text):
		"""
		Определение кодировки текста

		:param text:  текст
		:return:  кодировка
		"""
		return chardet.detect(text)['encoding']

	def encodeText(self, text, encoding='utf-8'):
		"""
		Перекодировка текста

		:param text:  текст
		:param encoding:  перевод текста в данную кодировку
		:return:  перекодированный текст
		"""
		textEncoding = self.getEncode(text)
		if textEncoding != encoding:
			return text.decode(textEncoding).encode(encoding)
		return text


class Normalization():
	""" Класс для нормализации текста """

	__metaclass__ = ABCMeta

	@abstractmethod
	def normalizeText(self, text):
		"""
		Нормализация текста

		:param text:  текст
		:return: список нормализованных слов (слова могут повторятся)
		"""
		return None

	@abstractmethod
	def normalizeTextWithoutRepetition(self, text):
		"""
		Нормализация текста без повторений

		:param text:  текст
		:return:  список нормализованных слов (без повторений)
		"""
		return None

	@abstractmethod
	def setNormalizeTextEncode(self, normalizeTextEncode):
		"""
		Установить кодировку нормализованного текста

		:param normalizeTextEncode:  название кодировки (например, utf-8)
		"""
		pass

	@abstractmethod
	def getNormalizeTextEncode(self):
		"""
		Получить кодировку нормализованного текста

		:return:  название кодировки (по-умолчанию что-то должно быть задано)
		"""
		return None

	normalizeTextEncode = abstractproperty(getNormalizeTextEncode, setNormalizeTextEncode)


class SimpleNormalization(Normalization):
	""" Класс реализующий простую нормализацию текста """

	def __init__(self):
		self.__detectEncoding = DetectEncoding()
		self.__defaultEncodeText = "utf-8"
		self.setNormalizeTextEncode(self.__defaultEncodeText)
		self.__diacritics = re.compile(u'[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]', re.U)
		self.__detection = Detection()
		self.__porterStemming = PorterStemming()

	def normalizeText(self, text):
		if not text:
			raise ParamError("Text is not to be None or ''")

		dt = self.__detectEncoding.encodeText(text, self.__defaultEncodeText)  # dt = decode text
		ndt = self.__diacritics.sub('', unicodedata.normalize('NFD', unicode(dt, self.__defaultEncodeText)))
		ndt = ndt.lower().replace("\n", " ").strip()

		n_w = []  # normalize words
		if ndt:
			temp_normalize_words = re.split('\s+', ndt)
			for word in temp_normalize_words:
				unicode_word = self.__normalize_word(word)

				lang = self.__detection.detect(unicode_word)
				normalize_word = unicode_word

				if lang == 1:
					normalize_word = self.__porterStemming.stem(unicode_word)
				elif lang == 2:
					normalize_word = self.__porterStemming.stemRu(unicode_word)

				# чтобы не добавлять пустые строки. Пример ""
				if normalize_word:
					n_w.append(normalize_word)
		else:
			try:
				n_w = re.split('\s+', ndt)
			except Exception as e:
				print("Error parse {0}".format(str(e)))

		return [self.__detectEncoding.encodeText(item.encode(self.__defaultEncodeText), self.getNormalizeTextEncode()) for item in n_w]

	def normalizeTextWithoutRepetition(self, text):
		return list(set(self.normalizeText(text)))

	def setNormalizeTextEncode(self, normalizeTextEncode):
		"""
		Установить кодировку для нормализованного текста

		:param normalizeTextEncode:  название кодировки (по-умолчанию utf-8)
		"""
		self.__normalizeTextEncode = normalizeTextEncode

	def getNormalizeTextEncode(self):
		"""
		Получить кодировку для нормализованного текста

		:return:  название кодировки (по умолчанию utf-8)
		"""
		return self.__normalizeTextEncode

	def __normalize_word(self, word):
		"""
		Убрать из начала и конца слова все символы не из алфавита

		:param word: слово
		:return: нормализованное слово
		"""

		unicode_word = word
		try:
			unicode_word = word.decode("utf-8")
		except UnicodeEncodeError:
			# print "UnicodeEncodeError"
			pass

		word_len = len(unicode_word)

		if word_len == 0:
			return unicode_word

		f_index = 0             # индекс первого символа
		s_index = word_len - 1  # индекс последнего символа

		# ищем позицию первого индекса
		for x in range(0, word_len):
			f_index = x
			if self.__detection.check_symbol(unicode_word[x]):
				break

		for x in range(s_index, f_index, -1):
			s_index = x
			if self.__detection.check_symbol(unicode_word[x]):
				break

		if f_index + 1 >= s_index:
			return unicode_word[f_index]

		return unicode_word[f_index: s_index + 1]

	normalizeTextEncode = property(getNormalizeTextEncode, setNormalizeTextEncode)
