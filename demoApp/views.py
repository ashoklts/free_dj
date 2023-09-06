from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
import http.client
import json


def gm_view(request):
    
    
    conn = http.client.HTTPSConnection("www.nseindia.com")


    headers = {
    'authority': "www.nseindia.com",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-language': "en-US,en;q=0.9,ta;q=0.8",
    'cache-control': "no-cache",
    'postman-token': "08c93e01-afd3-b93e-bfc8-1a8b1b2ef57a"
    }

    conn.request("GET", "/api/option-chain-indices?symbol=NIFTY", headers=headers)

    # res = conn.getresponse()
    # data = res.read()

    # print(data.decode("utf-8"))

    
    
    # url = "https://www.nseindia.com/option-chain"

    # headers = {
    #     'authority': "www.nseindia.com",
    #     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     'accept-language': "en-US,en;q=0.9,ta;q=0.8",
    #     'cache-control': "no-cache",
    #     'postman-token': "49a3e321-fd0c-56c4-85f7-49fdd3bb90cd"
    #     }

    # response = requests.request("GET", url, headers=headers)

    # print(response.text)
    return JsonResponse({"chain" : "test"}) #json.loads(data.decode("utf-8")) 

# Create your views here.
