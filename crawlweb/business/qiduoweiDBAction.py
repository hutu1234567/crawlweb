from crawlweb.framework.Action import DBAction
import pymysql

class QiduoweiDBAction(DBAction):
    @staticmethod
    def get_conn():
        conn = pymysql.connect( "10.110.1.245", "root", "v6root", "v6db", 3306 )
        conn.set_charset( "utf8" )
        return conn
    def get_table(self):
        return "qiduowei"
    def get_urls(self):
        sql="select url from " + self.get_table()
        conn = self.get_conn()
        cursor =conn.cursor()
        cursor.execute(sql)
        list = cursor.fetchall()
        cursor.close()
        conn.close()

        return list

if __name__ == '__main__':
    QiduoweiDBAction().run("bbb","ccc")