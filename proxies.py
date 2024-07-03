"""
configured in secrets.json, file should contain:
{
    "api_key":"your api key here",
    "country":"proxy country you want here"
}

api is at rapidapi: https://rapidapi.com/almann/api/proxy-list2
free version allows up to 1000 requests per month (~30/day)
"""

import requests
import json

def get_proxies():
    with open("secrets.json","r") as f:
        secrets = json.load(f)
        proxy_api = secrets["proxy_api"]
        country = secrets["country"]

    url = "https://proxy-list2.p.rapidapi.com/proxy/get"

    querystring = {"type":"http","country":country,"anonymity":"high"}

    headers = {
        "x-rapidapi-key": proxy_api,
        "x-rapidapi-host": "proxy-list2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    proxies = response.json()
    # TODO: check all proxies work and return filtered results accordingly

    return proxies

if __name__ == "__main__":
    proxies = get_proxy()
    for proxy in proxies:
        print(proxy)