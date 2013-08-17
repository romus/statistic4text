# -*- coding: utf-8 -*-

__author__ = 'romus'


# deprecated

# import os
# import pickle
# import codecs
# from ir.normalization.normalization import Normalization


# class Vector(object):
#     """
#     Класс для создания индекса для векторного ранжирования.
#     """
#
#     index_file_path = ''          # пусть к индекс файлам
#     prefix_doc_name = "doc_ind_"  # префикс, для формирования имен индексов для документов
#     index_path = ''               # путь к индексам
#     __docs_name = []              # имена индексов для документов
#     # __norm = Normalization()      # для нормализации строк
#     __ind_name = []               # список индекс документов по первой букве слова ['a', 'b', .....]
#     __indexed_doc_names = []      # имена документов, по которым были построены индексы
#
#     def __init__(self):
#         super(Vector, self).__init__()
#
#     def __add_words_to_dict(self, dict_add, lines, name_dock):
#         """
#         Добавить слова в словарь
#
#         :param dict_add: словарь для добавления
#         :param lines: строки со словами и частотами
#         """
#
#         for line in lines:
#             node_list = line.strip().split('-')
#
#             # если строка была формата "слово-частота_слова"
#             if len(node_list) == 2:
#                 try:
#                     # если слово есть в словаре
#                     if node_list[0] in dict_add:
#                         dict_add[node_list[0]][name_dock] = int(node_list[1])
#                     # если слова в словаре нет
#                     else:
#                         dict_add[node_list[0]] = {name_dock: int(node_list[1])}
#                 except ValueError:
#                     return {}
#             else:
#                 return {}
#
#         return dict_add
#
#     def __save_abc_dict(self, filename, save_dict):
#         """
#         Сохранение словаря в файл
#
#         :param filename: имя файла для сохранения
#         :param save_dict: словарь
#         """
#
#         if not save_dict or not filename:
#             return
#
#         # noinspection PyUnusedLocal
#         merge_save_dict = {}
#         # если такой словарь уже есть, то два словаря нужно замержить, а результат сохранить
#         if filename in self.__ind_name:
#             with open(self.index_path + filename, 'rb') as read_file:
#                 read_dict = pickle.load(read_file)
#
#                 for k, v in save_dict.items():
#                     if k in read_dict:  # если слово есть в обоих словарях
#                         read_dict[k] = dict(v.items() + read_dict[k].items())
#                     else:
#                         read_dict[k] = v
#
#                 merge_save_dict = read_dict
#         # если такого словаря нет, то просто нужно просто сохранить словарь
#         else:
#             self.__ind_name.append(filename)
#             merge_save_dict = save_dict
#
#         with open(self.index_path + filename, 'wb') as write_file:
#             pickle.dump(merge_save_dict, write_file, -1)  # -1 для компрессии
#
#     # noinspection PyBroadException
#     def make_doc_index(self, doc_name, lines_list):
#         """
#         Формирование индекса по документу
#
#         :param doc_name: имя документа
#         :param lines_list: список строк документа
#         """
#
#         if not doc_name or not lines_list:
#             return None
#
#         words_dict = {}  # словарь для слов из документа формата {"слово": частота_слова, ...}
#         for line in lines_list:
#             if not line:
#                 continue
#
#             words_line_list = self.__norm.normalize(line)
#
#             if words_line_list:  # Если список не пустой ([]), то добавим слова в словарь
#                 for word in words_line_list:
#                     if word in words_dict:  # если слово уже есть в словаре, то увеличим его частоту в документе
#                         words_dict[word] += 1
#                     else:  # если слова нет в словаре, то добавим его словарь с частотой равной 1
#                         words_dict[word] = 1
#
#         if words_dict:
#             full_file_name = None
#
#             try:
#                 full_file_name = self.index_file_path + self.prefix_doc_name + doc_name
#                 # запишем в индекс для файла формата:
#                 # a-next_index
#                 # amazon-10
#                 # где a - первая буква слова, next_index - номер строки со второй буквой слова,
#                 # amazon - слово, 10 - частота слова "amazon"
#                 with open(full_file_name, "w") as write_file:
#                     sorted_words = sorted(words_dict)
#                     first_symbol = sorted_words[0][0]
#
#                     # список со словами c частотами, у которых одинаковая первая буква
#                     # пример ["amazon-30", ...], где 30 - это частота
#                     abc_list = []
#
#                     for word in sorted_words:
#                         if word[0] != first_symbol:
#                             count_lines = len(abc_list)
#                             write_file.write("%(1)s-%(2)d\n%(3)s\n" % {"1": first_symbol.encode("utf-8"),
#                                                                        "2": count_lines,
#                                                                        "3": '\n'.join(abc_list).encode("utf-8")})
#                             # write_file.write(first_symbol + "-" + str(count_lines) + '\n' + '\n'.join(abc_list) + "\n")
#                             abc_list = []
#                             first_symbol = word[0]
#
#                         abc_list.append(word + '-' + str(words_dict[word]))
#
#                     if abc_list:
#                         write_file.write("%(1)s-%(2)d\n%(3)s\n" % {"1": first_symbol.encode("utf-8"),
#                                                                    "2": len(abc_list),
#                                                                    "3": '\n'.join(abc_list).encode("utf-8")})
#                         # write_file.write(first_symbol + "-" + str(len(abc_list)) + '\n' + '\n'.join(abc_list) + "\n")
#
#                 self.__docs_name.append(doc_name)
#             except Exception:
#                 if full_file_name and os.path.isfile(full_file_name):
#                     os.remove(full_file_name)
#
#     def __process_file(self, open_file, meta_line, doc_name):
#         """
#         Обработка данных из файла
#
#         :param open_file: ссылка на открытый файл
#         :param meta_line: строка формата "символ_начала_сло_в-количество_строк_для_чтения"
#         :param doc_name:
#         """
#
#         sym = meta_line[0]  # слова на какие начальные символы читаются, например если "a" - "amazon"
#         count_line = int(meta_line[2:])  # сколько строк со словами будет читаться
#         # noinspection PyUnusedLocal
#         lines = [open_file.next() for x in xrange(count_line)]
#         f_dict = self.__add_words_to_dict({}, lines, doc_name)  # сформируем словарь
#         self.__save_abc_dict(sym, f_dict)  # сохраним словарь
#
#     # noinspection PyUnusedLocal,PyBroadException
#     def make_abc_index(self):
#         """
#         Построение алфавитного индекса по индексам документов.
#         """
#         while True:
#             if len(self.__docs_name) == 0:
#                 break
#
#             open_file = None
#             full_file_name = self.index_file_path + self.prefix_doc_name + self.__docs_name[0]
#
#             try:
#                 open_file = codecs.open(full_file_name, "r", "utf-8")  # открытие временного индекса
#
#                 while True:  # должен быть StopIteration
#                     meta_line = open_file.next().strip()
#                     self.__process_file(open_file, meta_line, self.__docs_name[0])
#
#                 open_file.close()
#             except IOError as e:
#                 pass
#                 # print "File not found %(exc)s" % {"exc": str(e)}
#             except IndexError as e:
#                 pass
#                 # print "Index error"
#             except StopIteration as e:
#                 pass
#                 # print "Stop iteration"
#                 if open_file:
#                     open_file.close()
#                     # добавление файла, который точно проиндексирован
#                     self.__indexed_doc_names.append(self.__docs_name[0])
#             except Exception as e:
#                 pass
#                 # print "Other exception %(exc)s" % {"exc": str(e)}
#
#             try:
#                 os.remove(full_file_name)  # файла с временным индексом точно должен существовать, но все же
#             except Exception as e:
#                 pass
#
#             del self.__docs_name[0]
#
#     def get_index_files_count(self):
#         """
#         Получить количество файлов с индексом
#         """
#         return len(self.__ind_name)
#
#     def get_dict_by_index(self, index):
#         """
#
#         :param index: нормер индекса, например 1, 2, 0, -1
#         Получить по номеру индекса словарь вида:
#         {'onli': {'doc1': 2}, 'ok': {'doc2': 1}}
#
#         """
#
#         # noinspection PyUnusedLocal
#         dict_index = []
#         # noinspection PyBroadException
#         try:
#             with open(self.index_path + self.__ind_name[index], "rb") as read_file:
#                 dict_index = pickle.load(read_file)
#         except Exception:
#             pass
#
#         return dict_index
#
#     # noinspection PyBroadException
#     def delete_abc_index(self):
#         """
#         Удаление буквенного индекса.
#
#         """
#
#         while True:
#             if len(self.__ind_name) == 0:
#                 break
#
#             full_file_name = self.index_path + self.__ind_name[0]
#             try:
#                 os.remove(full_file_name)
#             except Exception:
#                 pass
#             del self.__ind_name[0]
#
#     def clear_indexed_doc_names(self):
#         """
#         Очистить список документов, по которым точно построен индекс
#         """
#
#         self.__indexed_doc_names = []
#
#     def get_indexed_doc_names(self):
#         """
#         Получить список документов, по которым точно построен индекс
#         """
#
#         return self.__indexed_doc_names



# Пример
# import chardet
# vector = Vector()
#
# with open("doc4", "r") as read_file:
#     data = read_file.read()
#     result = chardet.detect(data)
#     encoding = result['encoding']
#
#     if encoding != 'utf-8':
#         data = data.decode(encoding).encode("utf-8")
#     lines = data.split('\n')
#
#     vector.make_doc_index("doc4", lines)
#
# with open("doc3", "r") as read_file:
#     data = read_file.read()
#     result = chardet.detect(data)
#     encoding = result['encoding']
#
#     if encoding != 'utf-8':
#         data = data.decode(encoding).encode("utf-8")
#     lines = data.split('\n')
#
#     vector.make_doc_index("doc3", lines)
#
# vector.make_abc_index()
# d = vector.get_dict_by_index(0)
# print d
