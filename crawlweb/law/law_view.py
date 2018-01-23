from django.shortcuts import render
from django.http import request
def get_guid(request):
    return render( request,"get_guid.html")

def get_key(request):
    vjkl5 = request.GET.get("vjkl5")
    return render( request,"get_key.html")