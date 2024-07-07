import threading
import time
import requests
import random

from tornet import ma_ip, initialize_environment, change_ip_repeatedly

def initialize_tornet():
    initialize_environment()
    print("Tor environment initialized.")

def create_tor_session():
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    return session

def whats_my_ip():
    try:
        return ma_ip()
    except requests.RequestException as e:
        print(f"Error retrieving IP: {e}")
        return "Unknown"

def start_ip_changer(interval=1):
    try:
        change_ip_repeatedly(interval, 0)  # Change IP every `interval` seconds indefinitely
    except Exception as e:
        print(f"Error starting IP changer: {e}")

def load_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = file.readlines()
        proxies = [proxy.strip() for proxy in proxies]
        if not proxies:
            print("Proxy list is empty.")
        return proxies
    except FileNotFoundError:
        print(f"Proxy file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []


def get_random_proxy(proxies):
    if proxies:
        return random.choice(proxies)
    else:
        print("Proxy list is empty.")
        return None

def switch_proxy(proxies, interval=5):
    while True:
        if not proxies:
            print("No proxies available to switch.")
            break
        proxy = get_random_proxy(proxies)
        if proxy:
            print(f"Switching to proxy: {proxy}")
            return proxy
        time.sleep(interval)
       

# Proxy scraping functions
def scrape_proxies(api_url, file_name="proxies.txt"):
    """
    Download the proxy list from the API endpoint and save it to a file.
    Overwrite the file if it already exists.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        proxies = clean_proxies(response.text)
        save_proxies_to_file(proxies, file_name)
        print(f"Proxies downloaded and saved to {file_name}.")
    except requests.RequestException as e:
        print(f"Error downloading proxies: {e}")

def clean_proxies(proxies_text):
    """
    Remove leading and trailing whitespace from each line in the proxy list.
    """
    return "\n".join(line.strip() for line in proxies_text.splitlines() if line.strip())

def save_proxies_to_file(proxies, file_name):
    """
    Save the cleaned proxy list to a file, overwriting the file if it already exists.
    """
    try:
        with open(file_name, "w") as file:
            file.write(proxies)
        print(f"Proxies saved to {file_name}.")
    except Exception as e:
        print(f"Error saving proxies to file: {e}")

