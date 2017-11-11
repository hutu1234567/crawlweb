#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-03-12


from six import itervalues
import pymysql


class MySql():
    def __init__(self):

        hosts = '10.10.250.100'
        username = 'root'
        password = 'inspurcrawl'
        database = 'credit'
        charsets = 'utf8'

        self.connection = False
        try:
            self.conn = pymysql.connect(host=hosts, user=username, passwd=password, db=database, charset=charsets)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names " + charsets)
            self.connection = True
        except Exception as e:
            print("Cannot Connect To Mysql!/n", e)

    def escape(self, string):
        return '%s' % string

    def into(self, tablename=None, **values):

        if self.connection:
            tablename = self.escape(tablename)
            if values:
                _keys = ",".join(self.escape(k) for k in values)
                _values = ",".join(['%s', ] * len(values))
                sql_query = "insert into %s (%s) values (%s)" % (tablename, _keys, _values)
            else:
                sql_query = "replace into %s default values" % tablename
            try:
                if values:
                    self.cursor.execute(sql_query, list(itervalues(values)))
                else:
                    self.cursor.execute(sql_query)
                self.conn.commit()
                return True
            except Exception as e:
                print("An Error Occured: ", e)
                return False
