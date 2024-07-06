"""
configured in secrets.json, file should contain:
{
    "api_key":"your api key here",
    "country":"proxy country you want here"
}

api is at rapidapi: https://rapidapi.com/almann/api/proxy-list2
free version allows up to 1000 requests per month (~30/day)

improved: only request proxies if proxies.json is not the same country and date when checking to run - consumes less api uses
"""

import requests
import json
import os
from datetime import datetime

def get_proxies():
    with open("secrets.json","r") as f:
        data = json.load(f)
        proxy_api = data["proxy_api"]
        country = data["country"]

    current_date = datetime.now().strftime("%Y%m%d")  # YYYYMMDD string format
    new_proxies_required = True  # check if new proxy list from api is required
    if os.path.isfile("proxies.json"):
        with open("proxies.json","r") as f:
            data = json.load(f)
            existing_country = data["country"]
            date_created = data["date"]
            if existing_country == country and date_created == current_date:
                proxies = data["proxies"]  # retrieve generated list of proxies
                new_proxies_required = False
                print("using existing proxies.json file")

    if new_proxies_required == True:
        url = "https://proxy-list2.p.rapidapi.com/proxy/get"

        querystring = {"type":"http","country":country,"anonymity":"high"}

        headers = {
            "x-rapidapi-key": proxy_api,
            "x-rapidapi-host": "proxy-list2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        proxies = response.json()
        # TODO: check all proxies work and return filtered results accordingly

        # save proxies to file
        new_proxy_dict = {
            "country":country,
            "date":current_date,
            "proxies":proxies
        }
        print("creating new proxies.json file")
        with open("proxies.json","w", encoding="utf-8") as f:
            json.dump(new_proxy_dict,f,ensure_ascii=False,indent=4)

    return proxies

if __name__ == "__main__":
    proxies = get_proxies()
    for proxy in proxies:
        print(proxy)