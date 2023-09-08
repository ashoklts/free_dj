from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
import http.client
import json

from py5paisa import FivePaisaClient

import pyotp
import time
import math

# ashoklts
# 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

url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()



secret =  "GUYDMMRRGIYTQXZVKBDUWRKZ"  #pyotp.random_base32()
cred={
    "APP_NAME":"5P50621218",
    "APP_SOURCE":"15635",
    "USER_ID":"CZsJNvTY8Nn",
    "PASSWORD":"RtH02JIxjod",
    "USER_KEY":"5MEAGCtpGJIbxhcDinpMocDnvK230NUI",
    "ENCRYPTION_KEY":"VgMHQZrhfd7gR8Ul2TDn4ywvnB2LEH3j"
    }


def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    
def get_data(url):
    print('url',url)
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        # print(response.text)
        return response.text
    return ""

def gm_view(request):

    # response_text = get_data(url_bnf)
    # data = json.loads(response_text)
    # print
    
    totp = pyotp.TOTP(secret)
    tpin = totp.now() # => '492039'


    
    
    # client = FivePaisaClient(cred=cred)

    # # New TOTP based authentication
    # client.get_totp_session('50621218',tpin,'021092')
    # client.get_access_token(client.request_token)

    # print(client.access_token)
    
    
    client = FivePaisaClient(cred=cred)
    client.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwNjIxMjE4Iiwicm9sZSI6IjE1NjM1IiwiU3RhdGUiOiIiLCJSZWRpcmVjdFNlcnZlciI6IkMiLCJuYmYiOjE2OTQxNTIxNTYsImV4cCI6MTY5NDE5Nzc5OSwiaWF0IjoxNjk0MTUyMTU2fQ.eOUSSJq-Y3VNl8SOgGglClBBkwuiTVDcu8Tg6Q-PqDE";
    # print(client.holdings())
    expires = client.get_expiry("N","BANKNIFTY")
    print(expires['Expiry'][0]["ExpiryDate"])
    s = expires['Expiry'][0]["ExpiryDate"]
    first = "("
    last = "+0530)"
    start = s.rindex( first ) + len( first )
    end = s.rindex( last, start )
    print(s[start:end])
    

    get_op_chain = client.get_option_chain("N","BANKNIFTY",int(s[start:end]))
    
    # conn = http.client.HTTPSConnection("www.nseindia.com")

    # headers = {
    #     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     'accept-encoding': "gzip, deflate, br",
    #     'accept-language': "en-US,en;q=0.9,ta;q=0.8",
    #     'cache-control': "no-cache",
    #     # 'cookie': "_ga=GA1.1.314882651.1692424888; defaultLang=en; nsit=ZF81eZ5Y-x13e1uqrJX02nSO; AKA_A2=A; ak_bmsc=6A41F067BA444013E535628ACB70C351~000000000000000000000000000000~YAAQL5UvF4cFXj+KAQAAcIW6aBVgTChTpcwRA/oMaeJ2B8a9aiq5a9HiOSkf1B3awpK2J9+zALkGRGQIMnWYb2zhfTaPO63g8mPG5YTg3gfCHryknez/cX+yplfRjJZB0mFSSO2UK9Mxhwinn6rnWvXuP18eysOiRnbUrwnTk5rc2NOt4Rx1lwaXVCBxZmd6fgMoaxscvfcdLOTJJIYeZXQa+eGOyYBUGnsz3dHHPpHudXDdmlW4OlfTh4uSJVnqjwH9VCiOWAwKR7AuQfD/1Sy8XJM3XHpu4xrc2ADdO/Dhk1NWBl8g43WUTo944+LqrrV9QGaz767JEQyI56yOO9FNWA3XPfrrbCZIIXQG3u2gWzpck45kC4SyfzLYIRjIh8xzL4kuVpTxkduSMBU2Fuu7kSUTCi4d6A7WJ7b8jfsT1dyIkWN8K2M6GBiM/ht9NsmTG1SNuK3wGaU/npQ5EXGGN8eIdJYoibUnFSV1VXL1Nix2TUjWd8XbYgdp2HxDsb0u; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY5Mzk3NDU1NiwiZXhwIjoxNjkzOTgxNzU2fQ.WehG1uxfEYYDKXawxPGll_6Q8gB74Y77MXc-p2-8zYw; _ga_PJSKY6CFJH=GS1.1.1693974168.7.1.1693975315.60.0.0; RT=\"z=1&dm=nseindia.com&si=8cc127c4-24d9-46cc-a450-cb31336e7814&ss=lm78pp76&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d49.akstat.io%2F\"; bm_sv=750AFAE9E61ECF359B6D284A7B4B2D1E~YAAQBpUvF5HFfUqKAQAA5+fRaBWzZKtYtKBwME13WtJwyvfxEM9HmyZ/xklXGRqky2qRtav8q5VvRQy6Fbi0JFGHenmEvXQHimlvd8hn4Pn0c0VRlv0lnJTapyWfj0iGxJJA4nJV7WrU4cO4zwyDZeSWFPfXsKAkE5efy7PcCNm36pYTGILIyA5wjTf2WLBdC0F5sfP4bz/auh4z31x5nt/pbxSMv7ui73+2s4hLq8Lk58T0YAuw7ukGQratMp8vXIQlpA==~1",
    #     'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    #     'sec-ch-ua-mobile': "?0",
    #     'sec-ch-ua-platform': "\"Linux\"",
    #     'sec-fetch-dest': "document",
    #     'sec-fetch-mode': "navigate",
    #     'sec-fetch-site': "none",
    #     'sec-fetch-user': "?1",
    #     'upgrade-insecure-requests': "1",
    #     'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    #     'postman-token': "9ddefe51-2b8b-3c19-9f9b-112018950c91"
    #     }

    # conn.request("GET", "/api/option-chain-indices?symbol=NIFTY", headers=headers)

    # res = conn.getresponse()
    # data = res.read()

    # print(data.decode("utf-8"))
    
    
    # conn = http.client.HTTPSConnection("www.nseindia.com")


    # headers = {
    # 'authority': "www.nseindia.com",
    # 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # 'accept-language': "en-US,en;q=0.9,ta;q=0.8",
    # 'cache-control': "no-cache",
    # 'postman-token': "08c93e01-afd3-b93e-bfc8-1a8b1b2ef57a"
    # }
    
    # headers = {
    #     'authority' : 'www.nseindia.com',
    #     'path': '/api/option-chain-indices?symbol=NIFTY',
    #     'scheme': 'https',
    #     'accept'  : '*/*',
    #     'sec-fetch-site' : 'cross-site',
    #     'sec-fetch-mode' : 'cors',
    #     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     # 'accept-encoding': "gzip, deflate, br",
    #     'accept-language': "en-US,en;q=0.9,ta;q=0.8",
    #     'cache-control': "no-cache",
    #     'cookie': "_ga=GA1.1.314882651.1692424888; defaultLang=en; nsit=ZF81eZ5Y-x13e1uqrJX02nSO; AKA_A2=A; ak_bmsc=6A41F067BA444013E535628ACB70C351~000000000000000000000000000000~YAAQL5UvF4cFXj+KAQAAcIW6aBVgTChTpcwRA/oMaeJ2B8a9aiq5a9HiOSkf1B3awpK2J9+zALkGRGQIMnWYb2zhfTaPO63g8mPG5YTg3gfCHryknez/cX+yplfRjJZB0mFSSO2UK9Mxhwinn6rnWvXuP18eysOiRnbUrwnTk5rc2NOt4Rx1lwaXVCBxZmd6fgMoaxscvfcdLOTJJIYeZXQa+eGOyYBUGnsz3dHHPpHudXDdmlW4OlfTh4uSJVnqjwH9VCiOWAwKR7AuQfD/1Sy8XJM3XHpu4xrc2ADdO/Dhk1NWBl8g43WUTo944+LqrrV9QGaz767JEQyI56yOO9FNWA3XPfrrbCZIIXQG3u2gWzpck45kC4SyfzLYIRjIh8xzL4kuVpTxkduSMBU2Fuu7kSUTCi4d6A7WJ7b8jfsT1dyIkWN8K2M6GBiM/ht9NsmTG1SNuK3wGaU/npQ5EXGGN8eIdJYoibUnFSV1VXL1Nix2TUjWd8XbYgdp2HxDsb0u; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY5Mzk3NDU1NiwiZXhwIjoxNjkzOTgxNzU2fQ.WehG1uxfEYYDKXawxPGll_6Q8gB74Y77MXc-p2-8zYw; _ga_PJSKY6CFJH=GS1.1.1693974168.7.1.1693975315.60.0.0; RT=\"z=1&dm=nseindia.com&si=8cc127c4-24d9-46cc-a450-cb31336e7814&ss=lm78pp76&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d49.akstat.io%2F\"; bm_sv=750AFAE9E61ECF359B6D284A7B4B2D1E~YAAQBpUvF5HFfUqKAQAA5+fRaBWzZKtYtKBwME13WtJwyvfxEM9HmyZ/xklXGRqky2qRtav8q5VvRQy6Fbi0JFGHenmEvXQHimlvd8hn4Pn0c0VRlv0lnJTapyWfj0iGxJJA4nJV7WrU4cO4zwyDZeSWFPfXsKAkE5efy7PcCNm36pYTGILIyA5wjTf2WLBdC0F5sfP4bz/auh4z31x5nt/pbxSMv7ui73+2s4hLq8Lk58T0YAuw7ukGQratMp8vXIQlpA==~1",
    # }

    # conn.request("GET", "/api/option-chain-indices?symbol=NIFTY", headers=headers)

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
    return JsonResponse({"chain" : get_op_chain}) #json.loads(data.decode("utf-8")) 




def req_view(request):
    
    # import requests

    # url = "https://www.nseindia.com/api/option-chain-indices"

    # querystring = {"symbol":"NIFTY"}

    # headers = {
    #     'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     'accept-encoding': "gzip, deflate, br",
    #     'accept-language': "en-US,en;q=0.9,ta;q=0.8",
    #     'cache-control': "no-cache",
    #     'cookie': "_ga=GA1.1.314882651.1692424888; defaultLang=en; nsit=ZF81eZ5Y-x13e1uqrJX02nSO; AKA_A2=A; ak_bmsc=6A41F067BA444013E535628ACB70C351~000000000000000000000000000000~YAAQL5UvF4cFXj+KAQAAcIW6aBVgTChTpcwRA/oMaeJ2B8a9aiq5a9HiOSkf1B3awpK2J9+zALkGRGQIMnWYb2zhfTaPO63g8mPG5YTg3gfCHryknez/cX+yplfRjJZB0mFSSO2UK9Mxhwinn6rnWvXuP18eysOiRnbUrwnTk5rc2NOt4Rx1lwaXVCBxZmd6fgMoaxscvfcdLOTJJIYeZXQa+eGOyYBUGnsz3dHHPpHudXDdmlW4OlfTh4uSJVnqjwH9VCiOWAwKR7AuQfD/1Sy8XJM3XHpu4xrc2ADdO/Dhk1NWBl8g43WUTo944+LqrrV9QGaz767JEQyI56yOO9FNWA3XPfrrbCZIIXQG3u2gWzpck45kC4SyfzLYIRjIh8xzL4kuVpTxkduSMBU2Fuu7kSUTCi4d6A7WJ7b8jfsT1dyIkWN8K2M6GBiM/ht9NsmTG1SNuK3wGaU/npQ5EXGGN8eIdJYoibUnFSV1VXL1Nix2TUjWd8XbYgdp2HxDsb0u; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY5Mzk3NDU1NiwiZXhwIjoxNjkzOTgxNzU2fQ.WehG1uxfEYYDKXawxPGll_6Q8gB74Y77MXc-p2-8zYw; _ga_PJSKY6CFJH=GS1.1.1693974168.7.1.1693975315.60.0.0; RT=\"z=1&dm=nseindia.com&si=8cc127c4-24d9-46cc-a450-cb31336e7814&ss=lm78pp76&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d49.akstat.io%2F\"; bm_sv=750AFAE9E61ECF359B6D284A7B4B2D1E~YAAQBpUvF5HFfUqKAQAA5+fRaBWzZKtYtKBwME13WtJwyvfxEM9HmyZ/xklXGRqky2qRtav8q5VvRQy6Fbi0JFGHenmEvXQHimlvd8hn4Pn0c0VRlv0lnJTapyWfj0iGxJJA4nJV7WrU4cO4zwyDZeSWFPfXsKAkE5efy7PcCNm36pYTGILIyA5wjTf2WLBdC0F5sfP4bz/auh4z31x5nt/pbxSMv7ui73+2s4hLq8Lk58T0YAuw7ukGQratMp8vXIQlpA==~1",
    #     'sec-ch-ua': "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    #     'sec-ch-ua-mobile': "?0",
    #     'sec-ch-ua-platform': "\"Linux\"",
    #     'sec-fetch-dest': "document",
    #     'sec-fetch-mode': "navigate",
    #     'sec-fetch-site': "none",
    #     'sec-fetch-user': "?1",
    #     'upgrade-insecure-requests': "1",
    #     'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    #     'postman-token': "049db280-c63d-fc33-b508-2d93b12ca2a0"
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    return JsonResponse({"chain" : "test"}) #json.loads(data.decode("utf-8")) 

# Create your views here.
