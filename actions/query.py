# import requests
# requests.packages.urllib3.disable_warnings()
import httpx

from dotenv import dotenv_values
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# import urllib3 
# http = urllib3.PoolManager()
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}



def queryPoolAddress(baseTokenAddress, quoteTokenAddress):


    base = "https://api.geckoterminal.com/api/v2"
    network = config.get("NETWORK")
    tokens = baseTokenAddress+','+quoteTokenAddress
    # url = base+"/simple/networks/"+network+"/token_price/"+tokens
    dex = "uniswap-v3-sepolia-testnet"
    url = base+"/networks/"+network+"/dexes/"+dex+"/pools"
    # url = base + "/networks/" + network + "/dexes"
    params = {'base_token': 'WETH'}
    print(url)

    res = httpx.get(url, params=params)
    # print(x.json().data)
    # resp = urllib3.request("GET", base+"/networks")
    rtv = res.json()
    print(rtv)


# queryPoolAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14","0x0000000000000000000000000000000000000000")

def getEstimatedAmountOut(tokenIn, tokenOut, amountIn):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    symbols = tokenIn+","+tokenOut
    parameters = {
    'symbol':symbols,
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.get("CMC_KEY"),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price_1=data["data"][tokenIn][0]["quote"]["USD"]["price"]
        price_2=data["data"][tokenOut][0]["quote"]["USD"]["price"]
        amountOut = float(amountIn) * price_1 / price_2
        amountOut = str(round(amountOut, 6))
        print(price_1, price_2)
        
        print(amountOut)
        
        return amountOut
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None
        
