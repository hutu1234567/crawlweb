"""djangoDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from crawlweb import view,reptail_view
import crawlweb.stock.views as stockview
from django.contrib import admin
from crawlweb.books import bookview
urlpatterns = [
    url( r'^hello$', view.hello ),
    url( r'^admin', admin.site.urls ),
    url( r'^search/$',bookview.search),
    url( r'^stock_his/$',stockview.stock_his),
    url( r'^stock_list/$', stockview.stock_list ),
    url( r'^stock_search/$', stockview.stock_search ),
    url( r'^stock_his_query',reptail_view.query_stock_his),
]