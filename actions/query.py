# import requests
# requests.packages.urllib3.disable_warnings()
import httpx

from dotenv import dotenv_values

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


queryPoolAddress("0xfFf9976782d46CC05630D1f6eBAb18b2324d6B14","0x0000000000000000000000000000000000000000")
