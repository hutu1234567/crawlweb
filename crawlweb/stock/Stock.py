#http://q.stock.sohu.com/hisHq?code=cn_300651&start=19741206&end=20170612&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp&r=0.8515011509154788&0.2592917025404735
#简化为：http://q.stock.sohu.com/hisHq?code=cn_300651&start=19741206&end=20170612&period=d

from crawlweb.stock.StockParseAction import StockListParserAction
from crawlweb.framework.Action import BaseCaptureAction
from crawlweb.framework.Action import JsonParseAction
class StockHistory():

    def __init__(self,url):
        self.url=url
    def run(self):
        pass

if __name__ == '__main__':
    #StockHistory("http://q.stock.sohu.com/hisHq?code=cn_300651&start=19741206&end=20170612&period=d").run()
    ret=BaseCaptureAction("http://quote.eastmoney.com/stock_list.html").run()
    # val=JsonParseAction().run(ret)
    #ret=CaptureAction("http://www.baidu.com").run()

    #print(ret)
    # print(val)
    print(type(ret))
    #print(ret.content.decode("gbk"))
    html_code = ret.content.decode("gbk")
    #print(html_code)
    hp = StockListParserAction()
    hp.feed( html_code )
    hp.close()
    print( hp.links,len(hp.links) )
