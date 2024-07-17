import requests
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