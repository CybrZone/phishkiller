import concurrent.futures
import requests
import random
import string
import json

# Load configuration from config.json
def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

# Generate random email using names and domains from the config file
def generate_random_email(names, domains):
    name = random.choice(names)
    domain = random.choice(domains)
    return name + str(random.randint(1, 100)) + domain

# Generate random password of given length
def generate_random_password(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# Send POST requests continuously
def send_posts(url, names, domains, password_length, email_key, password_key):
    with requests.Session() as session:
        while True:
            email = generate_random_email(names, domains)
            password = generate_random_password(password_length)
            data = {
                email_key: email,
                password_key: password
            }
            response = session.post(url, data=data)
            print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}")

def main():
    # Load configuration
    config = load_config()
    url = config['url']
    num_threads = config['num_threads']
    names = config['users']
    password_length = config['password_length']
    domains = config['domain']
    email_key = config['email_key']
    password_key = config['password_key']

    # Use ThreadPoolExecutor to manage threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_posts, url, names, domains, password_length, email_key, password_key) for _ in range(num_threads)]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
