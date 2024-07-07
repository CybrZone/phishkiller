import threading
import requests
import random
import string
import names
import logging
import time
from fake_useragent import UserAgent
from Assets.emailHosts import weighted_email_domains


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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


def send_posts(url, session, num_posts_per_ip_change):
    current_ip = whats_my_ip()
    while True:
        if num_posts_per_ip_change == 1:
            new_ip = whats_my_ip()
            while new_ip == current_ip:
                time.sleep(1)
                new_ip = whats_my_ip()
            current_ip = new_ip
        
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}
        response = session.post(url, data=data, headers=headers)
        logging.info(
            f"Email: {email}, Password: {password}, Status Code: {response.status_code}, User-Agent: {user_agent}, IP: {current_ip}"
        )
        
        if num_posts_per_ip_change == 2:
            time.sleep(random.randint(5, 120))  # Random delay between 5 seconds and 2 minutes
        time.sleep(1)  # General delay to allow IP change

def main():
    initialize_tornet()
    
    url = input("Enter the URL of the target you want to flood: ")
    
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
    
    session = create_tor_session()
    
    if choice == 1:
        posting_thread = threading.Thread(target=send_posts, args=(url, session, 1), daemon=True)
        posting_thread.start()
    elif choice == 2:
        threads = [threading.Thread(target=send_posts, args=(url, session, 0), daemon=True) for _ in range(25)]
        for t in threads:
            t.start()
    elif choice == 3:
        posting_thread = threading.Thread(target=send_posts, args=(url, session, 2), daemon=True)
        posting_thread.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
