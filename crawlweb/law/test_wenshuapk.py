#_*_ coding:utf-8 _*_
import time
import random
import requests
import grequests
def getguid():
    return hex(int((random.random()+1)*0x10000))


if __name__ == '__main__':
    header1={
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Content-Length":"336",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie":"FSSBBIl1UgzbN7N80S=h9.yCCZCNhUv9XLQMQv6sOJ6pEdzVqvwJopzcO.ed67OMTRr1OCKVueFGh1WtUs1; FSSBBIl1UgzbN7N80T=1FjwO3YGbjofhKCc22byrqQx14YGfIV50Z0ONJeYo3uukDPBPCRfmt6rQlF1Amw0OVFj6oUqoIizDEyUJ6PcWiYWjos2s5OJ4vqgOmNMcEGoMqe4YfWNUlmbnYSXX_ecPlzx_2Ds5mgjpiyryAOqMo0Ii25VNYw9m8_Xyg81Cuo6a7dK3mTMm0ubhe.8RwTtxmFosZBgW0K6AlbDtH7WGACGUrxIz0qVU8GksLNdisp9ztXJb1aVg2_axG8hE7lTeAVHqas.sCBs3UKKLLe1OzCRwIwNmyV09p4ZZhxDArRbuzcOZuqYqSsTENJl1QLzUnZ3U8zC.HDBIvfRW8YRjHsHY; Hm_lvt_9e03c161142422698f5b0d82bf699727=1512107081; _gscu_125736681=12107080x3pcu742; _gscu_2116842793=95178964w3s95s65; __utma=61363882.1728912236.1513927561.1513927561.1513927561.1; __utmz=61363882.1513927561.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gscbrs_2116842793=1; ASP.NET_SessionId=gpebtfqu3jjablorphnguw3a; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1512981887,1513927570,1514269642,1514345404; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1514451780; vjkl5=b8ece9fff9b9c1501c818264d29b58620c6f5751",
        "Host":"wenshu.court.gov.cn",
        "Origin":"http://wenshu.court.gov.cn",
        "Referer":"http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%B1%B1%E4%B8%9C%E4%B8%AD%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2&conditions=searchWord+%E4%BA%A4%E9%80%9A%E4%BA%8B+++%E5%85%B3%E9%94%AE%E8%AF%8D:%E4%BA%A4%E9%80%9A%E4%BA%8B",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }

    header2={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "165",
    "Cookie": "FSSBBIl1UgzbN7N80S=h9.yCCZCNhUv9XLQMQv6sOJ6pEdzVqvwJopzcO.ed67OMTRr1OCKVueFGh1WtUs1; FSSBBIl1UgzbN7N80T=1FjwO3YGbjofhKCc22byrqQx14YGfIV50Z0ONJeYo3uukDPBPCRfmt6rQlF1Amw0OVFj6oUqoIizDEyUJ6PcWiYWjos2s5OJ4vqgOmNMcEGoMqe4YfWNUlmbnYSXX_ecPlzx_2Ds5mgjpiyryAOqMo0Ii25VNYw9m8_Xyg81Cuo6a7dK3mTMm0ubhe.8RwTtxmFosZBgW0K6AlbDtH7WGACGUrxIz0qVU8GksLNdisp9ztXJb1aVg2_axG8hE7lTeAVHqas.sCBs3UKKLLe1OzCRwIwNmyV09p4ZZhxDArRbuzcOZuqYqSsTENJl1QLzUnZ3U8zC.HDBIvfRW8YRjHsHY; Hm_lvt_9e03c161142422698f5b0d82bf699727=1512107081; _gscu_125736681=12107080x3pcu742; _gscu_2116842793=95178964w3s95s65; __utma=61363882.1728912236.1513927561.1513927561.1513927561.1; __utmz=61363882.1513927561.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gscbrs_2116842793=1; ASP.NET_SessionId=gpebtfqu3jjablorphnguw3a; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1512981887,1513927570,1514269642,1514345404; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1514455940",
    "Host": "wenshu.court.gov.cn",
    "Origin":"http://wenshu.court.gov.cn",
    "Upgrade-Insecure-Requests": "1",
    "Referer":"http://wenshu.court.gov.cn/list/list/?sorttype=1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
     "X-Requested-With":"XMLHttpRequest"
             }

    header3={
        "Content-Type":"application/json",
        "timespan":"20180102184938",
        "nonce":"24s2",
        "devid":"fae8eb570ada4285864e984a9580324b",
        "signature":"6e226f48acb7108c1702f4f02a19cc05",
        "User-Agent":"Dalvik/1.6.0 (Linux; U; Android 4.4.4; DUK-AL20 Build/KTU84P)",
        "Host":"wenshuapp.court.gov.cn",
        "Connection":"Keep-Alive",
        "Accept-Encoding":"gzip",
        "Content-Length":"71"

        #"Connection": "Keep-Alive",
        #"Accept-Encoding": "gzip",
        #"Content-Length": "258",

        #"Server": "360wzws",
        #"Date": "Tue, 02 Jan 2018 08:46:14 GMT",
        #"Content-Type": "application/json;charset=utf-8;",
        #"Content-Length": "4846",
        #"Connection": "keep-alive",
        #"X-Powered-By-360WZB": "wangzhan.360.cn",
        #"WZWS-RAY": "112-1514911574.411-s5shct",
    }
    #datas = {"dicval":"asc","reqtoken":"3e6b364779bdac949868b5a0cf1c0074","condition":"/CaseInfo/案/@法院层级=1 AND /CaseInfo/案/@案件类型=1 AND /CaseInfo/案//@文书类型=判决书","skip":"0","app":"cpws","limit":"20","dickey":"/CaseInfo/案/@法院层级"}
    datas = {"dicval": "asc", "reqtoken": "3e6b364779bdac949868b5a0cf1c0074",
              "skip": "0",
             "app": "cpws", "limit": "20"}

    getTokenData={"app":"cpws","devid":"fae8eb570ada4285864e984a9580324b","apptype":"1"}
    getTokenUrl="http://wenshuapp.court.gov.cn/MobileServices/GetToken"
    token=requests.post(getTokenUrl,data=getTokenData,headers=header3)
    print(token.reason)
    res = requests.post('http://wenshuapp.court.gov.cn/MobileServices/GetLawListData', data=datas, headers=header3)
    #res=requests.post('http://wenshu.court.gov.cn/List/ListContent',data=datas,headers=header1)
    #res=requests.post("http://wenshuapp.court.gov.cn/MobileServices/GetLawListData",data=datas,headers=header1)
    #res=grequests.get("http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%B1%B1%E4%B8%9C%E4%B8%AD%E7%BA%A7%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2&conditions=searchWord+%E4%BA%A4%E9%80%9A%E4%BA%8B+++%E5%85%B3%E9%94%AE%E8%AF%8D:%E4%BA%A4%E9%80%9A%E4%BA%8B",headers=header2)
    res=requests.post('http://wenshuapp.court.gov.cn/MobileServices/GetLawListData',data=datas,headers=header3)

    print(res.content)