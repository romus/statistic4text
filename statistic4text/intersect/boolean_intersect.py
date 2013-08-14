# -*- coding: utf-8 -*-

__author__ = 'romus'


class BooleanSearch(object):
    """
    Булевый поиск слов по индексу.
    В качестве булевой операции применяется логическое И.
    """

    k = 10                   # расстоние между словами
    max_string_length = 300  # максимальное количество символов в запросе
    __dict_list = []         # список словарей, которое нужно объединить
    __normal_list_dict = []  # нормализованный список словарей (на самом деле кортежей :) )

    def __init__(self):
        super(BooleanSearch, self).__init__()

    def __intersect(self, normal_dict1, normal_dict2):
        """
        Нахождение пересечения словарей.
        
        
        :rtype : объединенный словарь
        :param normal_dict1: нормализованный словарь, маска ниже
        :param normal_dict2: [частота_в_словаре, {док_ID: [частота_в_документе, словопозиции], ...}]
        Пример: [2, {1: [2, 10, 44]}]
        """

        intersect_dict = [0, {}]                               # словарь пересечения с учётом расстояния между словами
        sorted_key_dock1 = sorted(normal_dict1[1].iterkeys())  # сортировка по лексемам
        sorted_key_dock2 = sorted(normal_dict2[1].iterkeys())
        iter_dock1 = 0
        iter_dock2 = 0

        while True:
            try:
                name_dock1 = sorted_key_dock1[iter_dock1]  # получить имя n-документа из первого словаря
                name_dock2 = sorted_key_dock2[iter_dock2]  # получить имя n-документа из второго словаря
            except IndexError:
                return intersect_dict

            if name_dock1 < name_dock2:
                iter_dock1 += 1
            elif name_dock1 > name_dock2:
                iter_dock2 += 1
            else:
                indexList1 = normal_dict1[1][name_dock1]  # получить словопозиции для n-документа из первого словаря
                indexList2 = normal_dict2[1][name_dock2]  # получить словопозиции для n-документа из второго словаря
                intersectIndex = [0]  # словопозиции с учетом пересечения первого и второго списков а также расстояния k
                iter_indexList1 = 1                       # не с 0, потому что нулевой элемент - это частота
                iter_indexList2 = 1

                # сортировка словопозиций
                indexList1.sort()
                indexList2.sort()

                # слияние по словопозициям с учётом расстояния между словами (k)
                while iter_indexList1 < len(indexList1):
                    l = []                                                  # список со словопозициями во из второго словаря
                    while iter_indexList2 < len(indexList2):
                        if abs(indexList1[iter_indexList1] - indexList2[iter_indexList2]) <= self.k:
                            l.append(indexList2[iter_indexList2])
                        elif indexList2[iter_indexList2] > indexList1[iter_indexList1]:
                            break

                        iter_indexList2 += 1

                    if l:
                        intersectIndex.append(indexList1[iter_indexList1])  # добавляем словопозицию из первого словаря
                        intersectIndex += l                                 # добавляем словопозиции из второго словаря
                        intersectIndex[0] = len(intersectIndex) - 1
                        # noinspection PyUnusedLocal
                        l = []
                    iter_indexList1 += 1

                if len(intersectIndex) > 1:
                    intersect_dict[1][name_dock1] = intersectIndex
                    intersect_dict[0] += intersectIndex[0]

                iter_dock1 += 1
                iter_dock2 += 1

    def intersect(self, wordsDict):

        """
        Получить список документов.

        :param wordsDict: словарь пока хз какого формата (!!!)
        """

        intersectList = []
        try:
            wordsDict.sort(
                lambda x, y: cmp(len(x[1]), len(y[1])))  # сортировка словаря по количеству документов для каждого слова
            intersectList = wordsDict[0]
            wordsDict = wordsDict[1:]
        except IndexError:
            return intersectList

        while wordsDict:
            intersectList = self.__intersect(intersectList, wordsDict[0])
            wordsDict = wordsDict[1:]

        return intersectList
