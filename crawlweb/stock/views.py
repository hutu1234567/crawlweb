from django.http import JsonResponse,HttpResponse
import crawlweb.stock.Stock as Stock
from django.shortcuts import render
from crawlweb.stock.StockParseAction import StockListParserAction
import json

def stock_his(request):
    stock_code=request.GET.get("stock_code","")
    start_date = request.GET.get( "start_date", "" )
    end_date = request.GET.get( "end_date", "" )
    period = request.GET.get( "period", "" )

    # if(stock_code==""):
    #     return response.HttpResponse("{'success':'false','msg':'Please input stock code'}")
    print(stock_code)
    content=Stock.BaseAction("http://q.stock.sohu.com/hisHq?code=%s&start=%s&end=%s&period=%s"%(stock_code,start_date,end_date,period)).run()
    json_str=Stock.JsonParseAction().run(content)
    print("json_str=",json_str)
    response = JsonResponse( json_str, safe=False )
    response['Access-Control-Allow-Origin'] = '*'
    return response
    # if(not json_str["code"]==stock_code):
    #     return response.HttpResponse("{'success':'false','msg':'This stock code %s can't find any data'}"%(stock_code))
    #return JsonResponse(json_str)

def stock_list(request):
    content=Stock.BaseAction("http://quote.eastmoney.com/stock_list.html").run()
    html_code = content.decode("gbk").encode("utf-8")
    #print(type(html_code))
    hp = StockListParserAction()
    hp.feed( str(html_code,encoding="utf-8") )
    #hp.feed( html_code )
    hp.close()
    print(hp.links)
    print(hp.getJsonContent())
    response = JsonResponse( hp.getJsonContent(),safe=False,json_dumps_params={'ensure_ascii':False})# content_type='charset=utf-8' )
    # response.setCharacterEncoding("utf-8");

    return response

def stock_search(request):
    return render(request,"stock/stock_search.html")


