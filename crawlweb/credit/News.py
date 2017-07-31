#_*_ coding:utf-8 _*_

from crawlweb.framework.Action import BaseCaptureAction
from pyquery import PyQuery as PQ
from crawlweb.framework.Action import DBAction
import hashlib
import pymysql
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def crawl(url):
    #url = "http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042"
    # 以下为明细页面
    rep = BaseCaptureAction( url, sleeptime=0 ).run()
    # print(rep.content.decode("gbk"))
    pq = PQ( rep.content.decode( "gb2312" ) )
    content = pq( "#aspnetForm > div.Zjx_layout > div.Zjx_Right03 > div > div" )

    #content = PQ("<div><span>abc<p>ddd</p><a href=''>aa</a></div></span><img src='/a/b.jpg'></img>")
    #soup=BeautifulSoup( rep.content.decode( "gb2312" ))
    #print("soup=====")
    #print(soup.text)
    print( content )

    hasecode = hashlib.new( "md5", rep.content ).hexdigest()
    print( hasecode )
    news_title = pq( "#aspnetForm > div.Zjx_layout > div.Zjx_Right03 > div > div > h1" )
    print( "title==========" )
    print( news_title )

    print( "body==========" )
    html = "<div id=body>"
    body = abstract_content(url,content)
    print( body )
    html += body+"</div>"
    print(html)
    return html
    # news = News('www.cumetal.org.cn','中国金属材料流通协会',"http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042",rep.text,hasecode,news_title,str(news_body))
    # print(news.url)
    # NewsDbAction().run(news)
def abstract_content(url,content):
    #content# =  pq( "#aspnetForm > div.Zjx_layout > div.Zjx_Right03 > div > div > div" )
    #print( content.text() )
    #print( "text==========" )
    items = content.children()
    # print("type=====")
    # print( type( items[0] ) )
    body_html=""
    for item in items:
        print( "item text 1111====" )
        print( item .text)
        root_txt=item.text
        #item = content( item )
        temp_html=""
        if(len(item.getchildren())>0):

            print(item.text)
            print("has sub children")
#            print(item.attr("innerHTML"))
            temp_html = abstract_content(url,content(item))
            if(root_txt != None):
                body_html +="<p>"+root_txt+ temp_html+"</p>"
            else:
                body_html +=temp_html

            print("body_html=========="+body_html)
        else:
            print("have not children")
            print( "item=======" )
            #print( len( item.text() ) )
            if(item.text !=None):
                temp_html = item.text
            if(item.tail != None):
                temp_html += item.tail
            print( temp_html )
            #imgs = item.find( "img" )
            # print(len(imgs))
            if (item.tag=="img"):
                src = item.get("src") #img.attr( "src" )
                imghtml = str( PQ(item) )
                print( imghtml )
                newsrc = urljoin( url, src )
                imghtml = imghtml.replace( src, newsrc )
                temp_html += imghtml
                print("img======"+imghtml)
            if (item.tag == "a"):
                href = item.get( "href" )  # img.attr( "src" )
                item.set("href",value=urljoin( url, href ))
                href_html = str( PQ( item ) )
                print( href_html )
               # href_html = href_html.replace( href, newhref )
                temp_html += href_html
                print( "a href======" + href_html )
            if (temp_html.strip() != ""):
                body_html += "<p>" + temp_html + "</p>"
    return body_html
def crawlcnwood(url):
    rep = BaseCaptureAction( url, sleeptime=0 ).run()
    # print(rep.content.decode("gbk"))
    pq = PQ( rep.content.decode( "utf-8" ) )
    content = pq( "body > div.main > div.m_left3 > div.nr9" )
    print( content )

    hasecode = hashlib.new( "md5", rep.content ).hexdigest()
    print( hasecode )
    news_title = pq( "body > div.main > div.m_left3 > div.nr9 > h1" )
    print( "title==========" )
    print( news_title )
    body=abstract_content(url,content)
    return body

def crawlchinanzxh(url):
    #url = "http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042"
    # 以下为明细页面
    rep = BaseCaptureAction( url, sleeptime=0 ).run()
    # print(rep.content.decode("gbk"))
    pq = PQ( rep.content.decode( "utf-8" ) )
    content = pq( "body > div > div.quanju > div.cont > div" )
    print( content )

    hasecode = hashlib.new( "md5", rep.content ).hexdigest()
    print( hasecode )
    news_title = pq( "body > div > div.quanju > div.cont > div > div > div.title" )
    print( "title==========" )
    print( news_title )

    print( "body==========" )
    news_body = content#pq( "#aspnetForm > div.Zjx_layout > div.Zjx_Right03 > div > div > div" )
    print( news_body.text() )

    print( "text==========" )
    items = news_body.children()
    print( type( items[0] ) )
    html = "<div id=body>"
    for item in items:
        item = pq( item )
        print( "item=======" )
        print( len( item.text() ) )
        temp_html = item.text()
        # print( temp_html )
        imgs = item.find( "img" )
        # print(len(imgs))
        if (len( imgs ) > 0):
            for img in imgs:
                img = pq( img )
                print( "imgs======" )
                src = img.attr( "src" )
                imghtml = str( img )
                print( imghtml )
                newsrc = urljoin( url, src )
                imghtml = imghtml.replace( src, newsrc )
                temp_html += imghtml
                # print(imghtml)
        if (temp_html.strip() != ""):
            html = html + "<p>" + temp_html + "</p>"
    html += "</div>"

    print( html )
    # news = News('www.cumetal.org.cn','中国金属材料流通协会',"http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042",rep.text,hasecode,news_title,str(news_body))
    # print(news.url)
    # NewsDbAction().run(news)
class News():
    def __init__(self,domain_name,site_name,url,response,hashcode,title,body):
        self.domain_name = domain_name
        self.site_name = site_name
        self.url = url
        self.response = response
        self.hashcode = hashcode
        self.title = title
        self.body = body

class NewsDbAction(DBAction):
    @staticmethod
    def get_conn():
        conn = pymysql.connect( "10.110.1.245", "root", "v6root", "v6db", 3306 )
        conn.set_charset( "utf8" )
        return conn

    def run(self,value):
        #print(value)
        sql = "INSERT INTO %s (URL,CONTENT) VALUES('%s','%s')"%("js_news","aaaaa",value.response)
        print(sql)

        sql="INSERT INTO js_news (domain_name,site_name,url,response,hashcode,title,body) VALUES('%s','%s','%s','%s','%s','%s','%s')"%(value.domain_name,value.site_name,value.url,pymysql.escape_string(value.response),value.hashcode,value.title,pymysql.escape_string(value.body))
        print(sql)
        conn = self.get_conn()
        cursor = conn.cursor()
        # print(sql)
        ret = cursor.execute( sql )
        conn.commit()
        cursor.close();
        return ret

if __name__ == '__main__':
    #html=crawl("http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042")
    content = PQ("<div><span>abc<p>ddd</p><a href=''>aa</a>取得到<br/>取不得a<img src='/a/b.jpg'></img><br />取不到b</span></div>")


    html=abstract_content("http://www.baidu.com/aa",content)
    #html=crawlcnwood("http://www.cnwood.org/a/xinwenzixun/xiehuiyaowen/2017/0615/14975.html")
    #crawlchinanzxh("http://www.chinanzxh.com/index.php?m=content&c=index&a=show&catid=11&id=29740")
    print( "end html=====" )
    print( html )