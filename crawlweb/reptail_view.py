from django.shortcuts import render


def query_stock_his(request):

    content={}
    return render(request,"stock/stock_his_query.html",content)


def stock_his(request):
    content = {}
    return render( request, "stock/stock_his.html", content )
