import requests
import threading
import time
import sys
import random
import names
from Assets.emailHosts import weighted_email_domains
from ip_changer import whats_my_ip, initialize_tornet, create_tor_session, start_ip_changer

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

proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

def func_get_public_ip(): # Fetches the public IP address of the machine
    try:
        response = requests.get('https://icanhazip.com', proxies=proxies, headers={'User-Agent': func_get_random_user_agent(user_agents)})
        if response.status_code == 200:
            return response.text.strip()
        else:
            sys.exit(1)
            return None
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def name_gen():  # Generates a random name for the email
    name_system = random.choice(
        ["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"]
    )
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    if name_system == "FullName":  # JohnDoe
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":  # JohnD
        return first_name + last_name[0]
    return first_name[0] + last_name  # JDoe

def generate_random_email():
    # Generate email with combination of name and domain
    name = name_gen()
    use_number = random.choice([True, False])  # Renamed for clarity
    
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
    
    # Generate email with or without a number
    if use_number:
        return f"{name}{random.randint(1, 100)}{selected_domain}"
    else:
        return f"{name}{selected_domain}"


def generate_random_password():  # Generate password using uppercase, lowercase, numbers and special characters
    characters = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(12, 20)  # Random length between 12 and 20
    return "".join(random.choice(characters) for _ in range(length))

def func_attack(email, password, session, num_posts_per_ip_change): # Sends a POST request to the target URL with the email and password
    url = 'https://web.bit-box.digital/block-onauth.php'
    data = {'a': email, 'az': password}
    
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
        print(f"Sending : {get_agents[:50]} ...")
        response = session.post(url, data=data, proxies=proxies, headers=headers)
        print(f"Status code: {response.status_code}")

        if num_posts_per_ip_change == 2:
            time.sleep(random.randint(5, 120))  # Random delay between 5 seconds and 2 minutes
        time.sleep(1)  # General delay to allow IP change

    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
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
        print(f"Sending : {random_email[:50]} , {random_password[:50]} ...")

        # Send request
        session = create_tor_session()

        if choice == 1:
            posting_thread = threading.Thread(target=func_attack, args=(random_email, random_password, session, 1), daemon=True)
            posting_thread.start()
        elif choice == 2:
            threads = [threading.Thread(target=func_attack, args=(random_email, random_password, session, 0), daemon=True) for _ in range(25)]
            for t in threads:
                t.start()
        elif choice == 3:
            posting_thread = threading.Thread(target=func_attack, args=(random_email, random_password, session, 2), daemon=True)
            posting_thread.start()

        time.sleep(1)
        cycle_count += 1

    print("Finished 5 cycles. Restarting ...")
    sys.exit(0)