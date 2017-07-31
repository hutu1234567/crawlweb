import requests
import json
import pymysql
import abc
import time


class Action:
    pass

class BaseCaptureAction(Action):
    def __init__(self,url,timeout=3000,sleeptime=20):
        #默认每次请求都等3秒
        self.url=url
        self.timeout=timeout
        self.sleeptime=sleeptime
    def run(self):
        #req = urllib.request.Request(self.url)
        time.sleep(self.sleeptime)
        print("action url==="+self.url)
        return requests.get(self.url)
        #return urllib.request.urlopen(self.url,timeout=self.timeout).read()

class JsonParseAction(Action):

    def run(self,content):
        return json.loads(content)

class DBAction(Action):
    def run(self,url,content):
        content = pymysql.escape_string(content)
        sql = "INSERT INTO %s (URL,CONTENT) VALUES('%s','%s')"%(self.get_table(),url,content)
        print(sql)
        conn = self.get_conn()
        cursor = conn.cursor()
        #print(sql)
        ret = cursor.execute(sql)
        conn.commit()
        cursor.close();
        return ret

    @abc.abstractmethod
    def get_conn(self):
        pass

    @abc.abstractmethod
    def get_table(self):
        pass
if __name__ == '__main__':
    conn = pymysql.connect("10.110.1.245", "root", "v6root", "v6db", 3306)
    conn.set_charset( "utf8" )
    DBAction().run(conn,"qiduowei","aa","asdf")