# -*- coding: utf-8 -*-
import MySQLdb
import re
import datetime

__author__ = 'ennumramdan'

class QBuilder:
    def __init__(self):
        pass

    def select(self, table, fields='*', join="", where="", limit="", sort=""):
        global sql
        try:
            if join is None:
                join = ""
            if where is None:
                where = ""
            if limit is None:
                limit = ""
            if sort is None:
                sort = ""
            sql = u"""SELECT {} FROM {} {} {} {} {}""".format(fields, table, join, where, sort, limit)

            return sql
        except Exception:
            raise

    def delete(self, table, where):
        global sql
        try:
            sql = u"""DELETE FROM {} {}""".format(table, where)

            return sql
        except Exception:
            raise

    def insert(self, data, table_name, ignore=False):
        ignore_str = ""
        global sql
        if ignore:
            ignore_str = "IGNORE"
        try:
            keys = data.keys()
            fields = ", ".join(keys)

            sql = u"INSERT {} INTO {} (`{}`) " \
                  u"VALUES ({})".format(ignore_str, table_name, fields, self.value_insert(data, keys))

            return sql
        except Exception:
            raise

    def insert_update(self, data, key, table_name, exclude_field=''):
        global sql
        try:
            keys = data.keys()
            fields = "`, `".join(keys)

            sql = u"INSERT INTO {} (`{}`) " \
                  u"VALUES ({}) ON DUPLICATE KEY UPDATE {}".format(table_name, fields, self.value_insert(data, keys),
                                                                   self.value_update(data, key, exclude_field))

            return sql
        except Exception:
            raise

    def update(self, data, table, key):
        global sql
        try:
            sql = u"UPDATE {} SET {}  WHERE {} = '{}'".format(table, self.value_update(data, key), key, data[key])

            return sql
        except Exception:
            raise

    def value_insert(self, data, keys):
        values = list()
        for key in keys:
            if isinstance(data[key], unicode):
                values.append(u'"{0}"'.format(data[key].replace('"', '\\"')))
            elif data[key] is None or data[key] == "":
                values.append('NULL')
            elif self.is_number(data[key]) and str(data[key])[0] != '0':
                # handle for number phone too which is first number is '0'
                values.append(u'{0}'.format(data[key]))
            elif str(data[key]) == '0':
                values.append(u'{0}'.format(data[key]))
            elif type(data[key]) is datetime.datetime:
                values.append(u'"{0}"'.format(data[key].strftime("%Y-%m-%d %H:%M:%S")))
            elif type(data[key]) is datetime.date:
                values.append(u'"{0}"'.format(data[key].strftime("%Y-%m-%d")))
            else:
                try:
                    values.append(u'"{0}"'.format(MySQLdb.escape_string(str(data[key]))))
                except Exception, e:
                    values.append(u'"{0}"'.format(data[key].replace('"', '\\"')))
                    print e
                    pass

        value = u", ".join(values)
        return value

    def value_update(self, data, primary, exclude_field=''):
        try:
            primaries = primary.replace(' ', '').split(',')
            exclude_fields = exclude_field.replace(' ', '').split(',')
            sets = list()
            keys = data.keys()
            for key in keys:
                if key not in primaries or key not in exclude_fields:
                    if data[key] is not None and data[key] != "":
                        if isinstance(data[key], unicode):
                            sets.append(u'`{0}` = "{1}"'.format(str(key), data[key].replace('"','\\"')))
                        elif self.is_number(data[key]) and str(data[key])[0] != '0':
                            # handle for number phone too which is first number is '0'
                            sets.append(u'`{0}` = {1}'.format(str(key), data[key]))
                        elif str(data[key]) == '0':
                            sets.append(u'`{0}` = {1}'.format(str(key), data[key]))
                        elif type(data[key]) is datetime.datetime:
                            sets.append(u'`{0}` = "{1}"'.format(str(key), data[key].strftime("%Y-%m-%d %H:%M:%S")))
                        elif type(data[key]) is datetime.date:
                            sets.append(u'`{0}` = "{1}"'.format(str(key), data[key].strftime("%Y-%m-%d")))
                        else:
                            try:
                                sets.append(u'`{0}` = "{1}"'.format(str(key), MySQLdb.escape_string(str(data[key]))))
                            except Exception, e:
                                sets.append(u'`{0}` = "{1}"'.format(str(key), data[key].replace('"', '\\"')))
                                print e
                                pass
                    else:
                        sets.append(u'`{}` = NULL'.format(str(key)))

            return u", ".join(sets)
        except Exception, e:
            raise

    @staticmethod
    def is_number(s):
        if type(s) is str:
            intstr = ['Infinity', 'infinity', 'nan', 'inf', 'NAN', 'INF']
            if intstr.count(s.lower()) or re.match(r'[0-9]+(e|E)[0-9]+', s):
                return False

        try:
            float(s)
            return True
        except Exception:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except Exception:
            pass

        return False

    @staticmethod
    def clean_latin1(data):
        LATIN_1_CHARS = (
            (u'\xa0', ' '),
            (u'\xe2\x80\x99', "'"),
            (u'\xc3\xa9', 'e'),
            (u'\xe2\x80\x90', '-'),
            (u'\xe2\x80\x91', '-'),
            (u'\xe2\x80\x92', '-'),
            (u'\xe2\x80\x93', '-'),
            (u'\xe2\x80\x94', '-'),
            (u'\xe2\x80\x94', '-'),
            (u'\xe2\x80\x98', "'"),
            (u'\xe2\x80\x9b', "'"),
            (u'\xe2\x80\x9c', '"'),
            (u'\xe2\x80\x9c', '"'),
            (u'\xe2\x80\x9d', '"'),
            (u'\xe2\x80\x9e', '"'),
            (u'\xe2\x80\x9f', '"'),
            (u'\xe2\x80\xa6', '...'),
            (u'\xe2\x80\xb2', "'"),
            (u'\xe2\x80\xb3', "'"),
            (u'\xe2\x80\xb4', "'"),
            (u'\xe2\x80\xb5', "'"),
            (u'\xe2\x80\xb6', "'"),
            (u'\xe2\x80\xb7', "'"),
            (u'\xe2\x81\xba', "+"),
            (u'\xe2\x81\xbb', "-"),
            (u'\xe2\x81\xbc', "="),
            (u'\xe2\x81\xbd', "("),
            (u'\xe2\x81\xbe', ")"),
            (u'\xc3\xaf\xc2\x82', ""),
            (u'\xc2\xb0', "<sup>o</sup>"),
        )

        try:
            return data.encode('utf-8')
        except UnicodeDecodeError:
            data = data.decode('iso-8859-1')
            for _hex, _char in LATIN_1_CHARS:
                data = data.replace(_hex, _char)
            return data.encode('utf8')
