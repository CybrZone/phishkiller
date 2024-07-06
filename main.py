import ui
import threading
import requests
import random
import string
import names
import beaupy
from fake_useragent import UserAgent

hit = 0
def name_gen():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    if name_system == "FullName":
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":
        return first_name + last_name[0]
    return first_name[0] + last_name

def generate_random_email():
    name = name_gen()
    NumberOrNo = random.choice(["Number", "No"])
    domain = random.choice(["@gmail.com", "@yahoo.com", "@rambler.ru", "@protonmail.com", "@outlook.com", "@itunes.com"])
    if NumberOrNo == "Number":
        return name + str(random.randint(1, 100)) + domain
    else:
        return name + domain

def generate_random_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

def send_posts(url, number_of_posts):
    global hit
    for _ in range(number_of_posts):
        email = generate_random_email()
        password = generate_random_password()
        data = {"a": email, "az": password}
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent}

        try:
            response = requests.post(url, data=data, headers=headers)
            with hit_lock:  # Acquire lock before updating hit
                hit += 1
            print(f"Email: {email}, Password: {password}, Status Code: {response.status_code}, User-Agent: {user_agent}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")

def main():
    ui.show()
    ui.contrib()
    url = beaupy.prompt(
        prompt="[bold][white]Enter the URL of the target you want to flood: ",
        target_type=str,
        validator=lambda input: len(input) > 0,
        secure=False,
        raise_validation_fail=True,
        raise_type_conversion_fail=True,
        initial_value=None,
        completion=None
    )

    number_of_posts = int(beaupy.prompt(
        prompt="[yellow]Enter number of attacks to perform: ",
        target_type=int,
        validator=lambda input: input > 0,
        secure=False,
        raise_validation_fail=True,
        raise_type_conversion_fail=True,
        initial_value=None,
        completion=None
    ))

    # Call the function to send posts
    send_posts(url, number_of_posts)

    # Print total successful hits
    print(f"Total successful hits: {hit}")

if __name__ == "__main__":
    main()