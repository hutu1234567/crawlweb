#_*_ coding:utf-8 _*_

from crawlweb.framework.Action import BaseCaptureAction
from pyquery import PyQuery as PQ
from crawlweb.framework.Action import DBAction
import hashlib
import pymysql
from urllib.parse import urljoin
from lxml.html import HtmlComment


# cumetal demo :
# step 1: send request and receive respone
# step 2: init PQ Object
# step 3: get full news content and news title
# step 4: return full news content
def crawl_cumetal(url):
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

    hasecode = hashlib.new( "md5", rep.content ).hexdigest()#可以把整个网页html hash一下备存
    print( hasecode )
    news_title = pq( "#aspnetForm > div.Zjx_layout > div.Zjx_Right03 > div > div > h1" )
    print( "title==========" )
    print( news_title )

    return content

    # news = News('www.cumetal.org.cn','中国金属材料流通协会',"http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042",rep.text,hasecode,news_title,str(news_body))
    # print(news.url)
    # NewsDbAction().run(news)


#它会自行递归调用解析
def abstract_content(url,content):
    """
    Api Doc(API及参数说明)：
    本API的目的是将爬取到的网页HTML代码转换为更干净的HTML代码，消除css、注释等对无用内容，并将其中的url转换为全url，使整个html可直接预览、解析。
    
    features(已经实现的特性)：
        1、遍历html dom树，保留其结构和文本内容，去除css，已测试支持的元素包括：div span br a img p b
        2、去除htlm注释，如<!-- xxxxxx  -->
        3、将img元素的url转换为全路径
        4、将a元素的url转换为全路径
        5、支持标签内和标签后文本的保留，即text和tail属性
    
    Depend on(依赖)：
        依赖于第三方的pyquery、lxml，请使用前确保安装
    
    Parameters(参数)：
        url:该新闻原始的url
        content:需要清理的html内容，即新闻全文的内容，需要包装为PyQuery对象,必须包含在一个html元素内，比如<div>xxxxxxx</div>，而不能<div>xxx</div><span>asdf</span>
        
    Return(返回值):
        返回字符串，即清理后的html结果
    """
    cur_element_html = ""
    # 将本节点的文本和tail先预存一下，算完子节点后，还需要再追加上它们

    print("cur_node=====")
    print(str(content))
    cur_node = content[0]
    if cur_node.text is None:
        cur_node_txt = ""
    else:
        cur_node_txt = cur_node.text
    if cur_node.tail is None:
        cur_node_tail = ""
    else:
        cur_node_tail = cur_node.tail
    if type(cur_node) is HtmlComment:#把注释跳过
        print("here is a comment!!!!")
        return ""
    items = content.children()
    item_html = ""#item_html用来保存元素的纯html代码
    if len(items) > 0:#如果有子元素时，要先算里面的子元素
        for item in items:
            # print("item text 1111====")
            # print(item .text)
            # #item = content( item )
            # print(item.text)
            # print("have sub children")
#           print(item.attr("innerHTML"))
            item_html += abstract_content(url,content(item))#递归调用

            #cur_element_html += "<%s>"%item.tag+ root_txt + item_html + "</%s>"%item.tag + root_tail
            # print("cur_element_html=========="+item_html)
        cur_element_html = "<%s>"%cur_node.tag + cur_node_txt + item_html + "</%s>"%cur_node.tag + cur_node_tail#得出本元素及其子元素的html代码
    else:
        # print("have not children")
        if (cur_node.tag == "img"):#图片单独处理，替换src为全路径
            src = cur_node.get("src") #img.attr( "src" )
            cur_node.set("src",value=urljoin( url, src ))#计算全路径的url
            imghtml = str(PQ(cur_node))
            item_html = imghtml
            #经调试确认，不需要额外再补tail了！！！！保留这段代码，以备忘！！！
            # if (item.tail != None):#需要补上图片后的文字
            #     item_html += item.tail
            print("img======"+imghtml)
        elif(cur_node.tag == "a"):#超连接单独处理，替换src为全路径
            href = cur_node.get( "href" )  # img.attr( "src" )
            cur_node.set("href",value=urljoin( url, href ))#计算全路径的url
            href_html = str(PQ(cur_node))
            print( href_html )
            item_html = href_html
            #经调试确认，不需要额外再补tail了！！！！保留这段代码，以备忘！！！
            #if (item.tail != None):#需要补上超链接后的文字
            #    item_html += item.tail
            print( "a href======" + href_html )
        else:
            #非图片和超链接元素视为文字元素，进行一般文本处理，需要把标签内文本和标签后文本都保留下来
            inside_text=""
            tail_text=""
            print(cur_node.text)
            if (cur_node.text != None):
                inside_text = cur_node.text#标签内的文本
            if (cur_node.tail != None):
                tail_text = cur_node.tail#标签后的文本
            if (cur_node.tag == "br"):#换行符要单独处理，它不是<br></br>的包围形式
                item_html = inside_text + "<br/>" + tail_text#此处<br/>的写法遵循新的html规范，避免不再被支持。
            else:
                item_html += "<%s>"%cur_node.tag + inside_text + "</%s>"%cur_node.tag + tail_text#即<p>texta</p>textb的格式

                #cur_element_html += item_html#在内容html中追加上新处理过的信息
        cur_element_html = item_html
    return cur_element_html


def crawl_cnwood(url):
    rep = BaseCaptureAction(url, sleeptime=0 ).run()
    # print(rep.content.decode("gbk"))
    pq = PQ( rep.content.decode( "utf-8" ) )
    content = pq( "body > div.main > div.m_left3 > div.nr9" )
    print( content )

    hasecode = hashlib.new( "md5", rep.content ).hexdigest()
    print( hasecode )
    news_title = pq( "body > div.main > div.m_left3 > div.nr9 > h1" )
    print( "title==========" )
    print( news_title )
    return content


#chinanzxh Demo
def crawl_chinanzxh(url):
    #url = "http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042"
    # 以下为明细页面
    rep = BaseCaptureAction( url, sleeptime=0 ).run()
    # print(rep.content.decode("gbk"))
    pq = PQ( rep.content.decode( "utf-8" ) )
    content = pq( "body > div > div.quanju > div.cont > div" )
    print(content)

    #hasecode = hashlib.new( "md5", rep.content ).hexdigest()
    #print( hasecode )
    news_title = pq( "body > div > div.quanju > div.cont > div > div > div.title" )
    print( "title==========" )
    print( news_title )
    return content

    '''
    以下为原实现，用pyquery有些元素信息不便于获取，后改用htmlelement.
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
    '''
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

    # step 4: call abstract_content get html dom and content,ignore css and script
    #url = "http://www.baidu.com/aa"
    #content = PQ("<div><span>abc<p>ddd</p>链&nbsp;接前<a href=''>aa</a>&nbsp;&nbsp;&nbsp;&nbsp;链接后<br/>取不得a<img src='/a/b.jpg'></img>图片后的文字<br />取不到b</span></div>")    #单元调试用代码
    #body_html=abstract_content(url,content)#单元调试用代码

    url1="http://www.cumetal.org.cn/page/newsview.aspx?lmdm=gjgc&newid=8042"
    content = crawl_cumetal(url1)

    #url="http://www.cnwood.org/a/xinwenzixun/xiehuiyaowen/2017/0615/14975.html"
    #content=crawl_cnwood(url)
    #url1 = "http://www.chinanzxh.com/index.php?m=content&c=index&a=show&catid=11&id=29740"
    #content = crawl_chinanzxh( url1 )

    body_html = abstract_content( url1, content )#得到了清理后的html

    print("original news body html start======")
    print(content)
    print("original news body html end======")
    print("final news body html start=====" )
    print(body_html)
    print("final news body html end=====" )

    #可以通过以下方式来判断是否有文字丢失的情况，建议大家在爬取时也验证一下，避免处理过程中遗漏实际文本内容
    print("original text=====")
    print(PQ(body_html).text())
    print("final text=====")
    print(content.text())
    print(PQ(body_html).text()==content.text())