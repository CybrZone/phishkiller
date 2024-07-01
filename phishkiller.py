import concurrent.futures
import requests
import random
import string
import json
from tqdm import tqdm
import itertools

from fake_useragent import UserAgent

# Load configuration from config.json
def load_config(config_file="./config.json"):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Configuration file not found.")
        raise
    except json.JSONDecodeError:
        print("Error decoding the configuration file.")
        raise

# Generate a random email using names and domains from the config file
def generate_random_email(names, domains):
    name = random.choice(names)
    domain = random.choice(domains)
    return f"{name}{random.randint(1, 100)}{domain}"

# Generate a random password of a given length
def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Send POST requests continuously
def send_posts(url, names, domains, password_length, email_key, password_key, progress_bar, proxies):
    with requests.Session() as session:
        for _ in progress_bar:
            email = generate_random_email(names, domains)
            password = generate_random_password(password_length)
            data = {
                email_key: email,
                password_key: password
            }
            try:
                ua = UserAgent()
                user_agent = ua.random
                headers = {'User-Agent': user_agent}
                proxy = random.choice(proxies)
                response = session.post(url, data=data, headers=headers, proxies={"http": f"http://{proxy}"})
    
                progress_bar.set_postfix(email=email, status_code=response.status_code)
            except requests.RequestException as e:
                progress_bar.set_postfix(error=str(e))
            progress_bar.update(1)

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
    proxies = config['proxys']
    data_amount = config['data_amount']  # placebo at the moment, implement latter

    total_requests = data_amount  # Default to 1000 if not specified

        
    # Use ThreadPoolExecutor to manage threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Create a single progress bar for all threads
        with tqdm(total=total_requests, desc="Sending POST requests") as progress_bar:
            progress_bars = itertools.cycle([progress_bar])
            futures = [
                executor.submit(send_posts, url, names, domains, password_length, email_key, password_key, progress_bar, proxies)
                for progress_bar in itertools.islice(progress_bars, num_threads)
            ]
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
