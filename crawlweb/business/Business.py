# coding:utf-8
from crawlweb.framework.Action import BaseCaptureAction
from crawlweb.business.qiduoweiDBAction import QiduoweiDBAction
from pyquery import PyQuery as PQ
import time


class QiduoweiSearchByKey(BaseCaptureAction):
    baseUrl = "http://www.qiduowei.com/search?key="
    @staticmethod
    def makeUrl(key,p=""):
        url = QiduoweiSearchByKey.baseUrl + key
        if p!="":
            url +="&p=" + p
        return url


if __name__ == '__main__':
    ret = QiduoweiDBAction().get_urls()
    except_com_list=[]
    for comid in ret:
        except_com_list.append(comid[0])
    keyVs = ["五金","钢铁","教育","通信","能源","投资","银行","科技","安全","交通","建筑"]
    for keyV in keyVs:
        url = QiduoweiSearchByKey.makeUrl(keyV)
        rep = QiduoweiSearchByKey(url).run()
        p = PQ(rep.content.decode("utf-8"))
        items=p('body > div.wrap.wrap-index > div > div > div > div.main-left > div.sort-section > div.result-tip > b')
        #print("items=",items)
        count = int(str(items.text().replace(",","")))
        page_number = count/20
        if(page_number>10):
            page_number=10
        for pageindex in range(1,page_number+1):#page_number+1):
            url = QiduoweiSearchByKey.makeUrl( keyV,str(pageindex))
            searchHtml = QiduoweiSearchByKey( url ).run().text
            print(searchHtml)
            print("是否过于频繁",searchHtml.find("过于频繁"))
            if searchHtml.find("过于频繁")>-1:
                print( pageindex + " 查询页，过于频繁" )
                time.sleep(100)
                break
            searchList=PQ(searchHtml)
            list = searchList('body > div.wrap.wrap-index > div > div > div > div.main-left > div.main > div.main-list ')
            hrefs = PQ(list).items("a")
            for item in hrefs:
                #print("item====",item)
                if(item.attr("class")=="company-name"):
                    href = item.attr("href")
                    com_url = "http://www.qiduowei.com" + href
                    if not com_url in except_com_list:
                        except_com_list.append(com_url)
                        company = BaseCaptureAction(com_url).run().text
                        if company.find("过于频繁")>-1:
                            #print( company.find( "过于频繁" ) )
                            print( com_url + " 过于频繁" )
                            #print( company )
                        else:
                            print(QiduoweiDBAction().run(com_url,company))
                    else:
                        print(com_url +" already crawled")
            #print("list=====",href)
            #print(searchList)
        #print(p)