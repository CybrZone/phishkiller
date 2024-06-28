import random
import string
import requests
import threading
from faker import Faker


# List of names to generate email addresses
# names = ["alice", "bob", "charlie", "dave", "eve" "fred", "george",
#           "harry", "ivan", "james", "kyle", "larry", "mike", "noah", "oliver", "peter", 
#           "quincy", "ricky", "samuel", "tom", "ulysses", "victor", "wesley", "xavier", 
#           "yusuf", "zachary",
#           ]

domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@live.com"]

def generate_random_email(f):
    name = f.name()
    name = name.lower().replace(' ', '')
    middle = random.choice(['_', '.', ''])
    number = random.randint(1, 99)
    domain = random.choice(domains)
    return f"{name}{middle}{number}{domain}"

def generate_random_password():
    # Generate a random password of length 8
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(8))

def send_posts(url, location):
    f = Faker(location)
    while True:
        email = generate_random_email(f)
        password = generate_random_password()
        data = {
            "a": email,
            "az": password
        }
        response = requests.post(url, data=data)
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}")

def main():
    # Ask user for URL to flood
    URL = input("Enter the URL of the target you want to flood: ")

    threads = []
    locations = ["en_US", "en_GB", "it_IT", "en_IE"]
    for i in range(50):
        location = random.choice(locations)
        t = threading.Thread(target=send_posts, args=(URL,location,))
        # t.daemon = True
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
