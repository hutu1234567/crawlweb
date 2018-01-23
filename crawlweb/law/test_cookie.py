import http.cookiejar, urllib.request
import requests

if __name__ == '__main__':

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = opener.open("http://www.baidu.com")
    a=requests.utils.dict_from_cookiejar(cj)
    print(a)