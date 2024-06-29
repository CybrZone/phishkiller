import threading
import requests
import random
import string
import os
os.system("pip install Faker")
from faker import Faker
fake = Faker()
# List of names to generate email addresses


def generate_random_email(name):
    if not name:
        name = fake.name()
    domain = "@gmail.com"  # You can change this domain
    return name.replace(" ",random.choice([".","",]) + str(random.randint(1, 100)) + domain

def generate_random_password(name):
    # Generate a random password of length 8
    if not name:
        name = fake.name()
    name=name.split(" ")
    letters_and_digits = string.ascii_letters + string.digits
    return random.choice(name) +''.join(random.choice(letters_and_digits) for i in range(random.randint(1, 4)))+random.choice([*name,""])

def send_posts(url,user="a",password="az"):
    while True:
        name = fake.name()
        email = generate_random_email(name)
        password = generate_random_password(name)
        data = {
            user: email,
            password: password
        }
        response = requests.post(url, data=data)
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}")

def main():
    # Ask user for URL to flood
    url = input("Enter the URL of the target you want to flood: ")
    user=input("Enter key of or email (Default:a): ")
    password=input("Enter key of password (Default:az): ")
    noOfThread=int(input("Enter no of worker(thread) at a time (hint: use your max no of cpu core)(Default:8): "))
    noOfFakeData=int(input("No of fake data to be added (Default:10,000)"))
    if not user:
        user=None
    if not password:
        password=None
    if not noOfThread:
        noOfThread=8
    if not noOfFakeData:
        noOfFakeData=10_000
    if url=="":
        url="https://haquegrp.com/xl/ecc2.php"
    threads = []
    
    for i in range(noOfFakeData):
        if threading.active_count()-1<noOfThread:
            t = threading.Thread(target=send_posts, args=(url,user,password))
            t.daemon = True
            t.start()
            threads.append(t)
        else:
            send_posts(url,user,password)


    for i in threads:
        i.join()

if __name__ == "__main__":
    main()
