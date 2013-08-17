# -*- coding: utf-8 -*-


__author__ = 'romus'


class ParamError(Exception):
	def __init__(self, *args, **kwargs):
		super(ParamError, self).__init__(*args, **kwargs)