# -*- coding: utf-8 -*-

__author__ = 'romus'

import re
from ir.stemming.porter import stem


class PorterStemming(object):
    __PERFECTIVEGROUND = re.compile(unicode('((ив|ивши|ившись|ыв|ывши|ывшись)|(([ая])(в|вши|вшись)))$', "UTF-8"))
    __REFLEXIVE = re.compile(unicode('(с[яь])$', "UTF-8"))
    __ADJECTIVE = re.compile(
        unicode('(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$', "UTF-8"))
    __PARTICIPLE = re.compile(unicode('((ивш|ывш|ующ)|(([ая])(ем|нн|вш|ющ|щ)))$', "UTF-8"))
    __VERB = re.compile(unicode(
        '((ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|(([ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)))$',
        "UTF-8"))
    __NOUN = re.compile(unicode(
        '(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$',
        "UTF-8"))
    __RVRE = re.compile(unicode('^(.*?[аеиоуыэюя])(.*)$', "UTF-8"))
    __DERIVATIONAL = re.compile(unicode('.*[^аеиоуыэюя]+[аеиоуыэюя].*ость?$', "UTF-8"))
    __DER = re.compile(unicode('ость?$', "UTF-8"))
    __SUPERLATIVE = re.compile(unicode('(ейше|ейш)$', "UTF-8"))
    __I = re.compile(unicode('и$', "UTF-8"))
    __P = re.compile(unicode('ь$', "UTF-8"))
    __NN = re.compile(unicode('нн$', "UTF-8"))

    def __init__(self):
        super(PorterStemming, self).__init__()

    def stemRu(self, word):
        word = word.lower().replace(unicode('ё', "UTF-8"), unicode('е', "UTF-8"))
        m = self.__RVRE.match(word)

        if m:
            pre = m.group(1)
            rv = m.group(2)
            temp = self.__PERFECTIVEGROUND.sub('', rv, 1)
            if temp == rv:
                rv = self.__REFLEXIVE.sub('', rv, 1)
                temp = self.__ADJECTIVE.sub('', rv, 1)
                if temp != rv:
                    rv = temp
                    rv = self.__PARTICIPLE.sub('', rv, 1)
                else:
                    temp = self.__VERB.sub('', rv, 1)
                    if temp == rv:
                        rv = self.__NOUN.sub('', rv, 1)
                    else:
                        rv = temp
            else:
                rv = temp

            rv = self.__I.sub('', rv, 1)

            if self.__DERIVATIONAL.match(rv):
                rv = self.__DER.sub('', rv, 1)

            temp = self.__P.sub('', rv, 1)

            if temp == rv:
                rv = self.__SUPERLATIVE.sub('', rv, 1)
                rv = self.__NN.sub('', rv, 1)
            else:
                rv = temp

            word = pre + rv

        return word

    def stem(self, word):
        return stem(word)
