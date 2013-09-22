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
		self._detectEncoding = DetectEncoding()
		self._defaultEncodeText = "utf-8"
		self.setNormalizeTextEncode(self._defaultEncodeText)
		self._diacritics = re.compile(u'[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]', re.U)
		self._detection = Detection()
		self._porterStemming = PorterStemming()

	def normalizeText(self, text):
		if not text:
			raise ParamError("Text is not to be None or ''")

		dt = self._detectEncoding.encodeText(text, self._defaultEncodeText)  # dt = decode text
		ndt = self._diacritics.sub('', unicodedata.normalize('NFD', unicode(dt, self._defaultEncodeText)))
		ndt = ndt.lower().replace("\n", " ").strip()

		n_w = []  # normalize words
		if ndt:
			temp_normalize_words = re.split('\s+', ndt)
			for word in temp_normalize_words:
				unicode_word = self._normalizeWord(word)

				lang = self._detection.detect(unicode_word)
				normalize_word = unicode_word

				if lang == 1:
					normalize_word = self._porterStemming.stem(unicode_word)
				elif lang == 2:
					normalize_word = self._porterStemming.stemRu(unicode_word)

				# чтобы не добавлять пустые строки. Пример ""
				if normalize_word:
					n_w.append(normalize_word)
		else:
			try:
				n_w = re.split('\s+', ndt)
			except Exception as e:
				print("Error parse {0}".format(str(e)))

		return [self._detectEncoding.encodeText(item.encode(self._defaultEncodeText), self.getNormalizeTextEncode()) for item in n_w]

	def normalizeTextWithoutRepetition(self, text):
		return list(set(self.normalizeText(text)))

	def setNormalizeTextEncode(self, normalizeTextEncode):
		"""
		Установить кодировку для нормализованного текста

		:param normalizeTextEncode:  название кодировки (по-умолчанию utf-8)
		"""
		self._normalizeTextEncode = normalizeTextEncode

	def getNormalizeTextEncode(self):
		"""
		Получить кодировку для нормализованного текста

		:return:  название кодировки (по умолчанию utf-8)
		"""
		return self._normalizeTextEncode

	def _normalizeWord(self, word):
		"""
		Убрать из начала и конца слова все символы не из алфавита

		:param word: слово
		:return: нормализованное слово
		"""

		unicodeWord = word
		try:
			unicodeWord = word.decode("utf-8")
		except UnicodeEncodeError:
			# print "UnicodeEncodeError"
			pass

		wordLen = len(unicodeWord)

		if wordLen == 0:
			return unicodeWord

		f_index = 0             # индекс первого символа
		s_index = wordLen - 1  # индекс последнего символа

		# ищем позицию первого индекса
		for x in range(0, wordLen):
			f_index = x
			if self._detection.check_symbol(unicodeWord[x]):
				break

		for x in range(s_index, f_index, -1):
			s_index = x
			if self._detection.check_symbol(unicodeWord[x]):
				break

		if f_index + 1 >= s_index:
			return unicodeWord[f_index]

		return unicodeWord[f_index: s_index + 1]

	normalizeTextEncode = property(getNormalizeTextEncode, setNormalizeTextEncode)
