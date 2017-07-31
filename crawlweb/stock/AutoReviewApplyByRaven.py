import requests
import re
from html.parser import HTMLParser
import time
import random
import logging
import json

class ReviewListParserAction( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__( self )
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len( attrs ) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        if str(value).startswith("javascript:applyOfficial") or str(value).startswith("javascript:applyRss")  :
                            self.links.append(re.sub("\D","", value ))

class NewTraceListParserAction( HTMLParser ):
    def __init__(self):
        HTMLParser.__init__( self )
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len( attrs ) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        if str(value).startswith("javascript:applyNews") :
                            self.links.append(re.sub("\D","", value ))
if __name__ == '__main__':
    logging.basicConfig( level=logging.DEBUG,
                         # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                         # datefmt='%a, %d %b %Y %H:%M:%S',
                         filename='myapp.log',
                         filemode='w' )
    while(True):
        try:
            curtime=time.localtime()
            curhour=int(time.strftime("%H",curtime))
            logging.debug( time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime() ) )
            if curhour>=8:
                logging.debug("Start Send Request!")
                userMap = {"email": "xiaxueking@sina.com","password":"simnba"}
                rep=requests.post("http://raven.infoq.com/users/auth",data=userMap)
                sleeptime=random.randint( 3, 10 )
                logging.debug("sleeping for list:"+str(sleeptime))
                time.sleep(sleeptime  )
                #print(rep.text)
                cookies=rep.cookies

                rep=requests.get("http://raven.infoq.com/official/review/all",cookies=cookies)
                parser = ReviewListParserAction()
                parser.feed(rep.text)
                #parser.links= ['8816']#调试用代码
                logging.warning("preview list==" + str(parser.links))

                if(len(parser.links)>0):
                    sleeptime = random.randint( 5, 20 )
                    logging.debug( "sleeping for apply:"+ str(sleeptime))
                    time.sleep(sleeptime)
                    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
                    data={"id":parser.links[0]}
                    logging.debug( "Start Review Request!"+ str(data))
                    rep=requests.post("http://raven.infoq.com/official/review/apply",data=data,json=data,cookies=cookies,headers=headers)
                    logging.warning("apply review===" +rep.encoding+ rep.text)

                #以下为领取文章
                sleeptime = random.randint( 3, 5 )
                rep = requests.get( "http://raven.infoq.com/official/rss/articles", cookies=cookies )
                parser = ReviewListParserAction()
                parser.feed( rep.text )
                #parser.links= ['8683']#调试用代码
                logging.warning( "artical list==" + str( parser.links ) )
                if (len( parser.links ) > 0):
                    sleeptime = random.randint( 5, 20 )
                    logging.debug( "sleeping for apply:" + str( sleeptime ) )
                    time.sleep( sleeptime )
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
                    data = {"rssid": parser.links[0]}
                    logging.debug( "Start artical Request!" + str( data ) )
                    rep = requests.post( "http://raven.infoq.com/official/apply", data=data, json=data,
                                         cookies=cookies, headers=headers )
                    #rep.encoding='utf-8'
                    logging.warning("apply artical===" +rep.apparent_encoding+rep.content.__str__())
                    logging.warning("apply artical===" +json.dumps(json.loads(rep.content,encoding="utf-8")))

                    # 以下为领取新闻
                    sleeptime = random.randint( 3, 5 )
                    rep = requests.get( "http://raven.infoq.com/official/rss/news", cookies=cookies )
                    parser = ReviewListParserAction()
                    parser.feed( rep.text )
                    # parser.links= ['8683']#调试用代码
                    logging.warning( "new list==" + str( parser.links ) )
                    if (len( parser.links ) > 0):
                        sleeptime = random.randint( 5, 20 )
                        logging.debug( "sleeping for apply:" + str( sleeptime ) )
                        time.sleep( sleeptime )
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
                        data = {"rssid": parser.links[0]}
                        logging.debug( "Start artical Request!" + str( data ) )
                        rep = requests.post( "http://raven.infoq.com/official/apply", data=data, json=data,
                                             cookies=cookies, headers=headers )
                        # rep.encoding='utf-8'
                        logging.warning( "apply new===" + rep.apparent_encoding + rep.content.__str__() )
                        logging.warning(
                            "apply new===" + json.dumps( json.loads( rep.content, encoding="utf-8" ) ) )
            else:
                logging.debug( "Skip Send Request!")
            sleeptime = random.randint( 60, 300 )
            logging.debug( "sleeping for close:"+ str(sleeptime))
            time.sleep(sleeptime)
            s=requests.session()
            s.keep_alive = False
            s.close()
            interval = random.randint(1800,2400)
            time.sleep(interval)
        except Exception as e:
            logging.error(e)
            s = requests.session()
            s.keep_alive = False
            s.close()