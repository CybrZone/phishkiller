import requests
import threading
import random
from fake_useragent import UserAgent
from loguru import logger
from credentials import CredentialGenerator


MAX_THREADS = 25
user_agent = UserAgent()
credential_generator = CredentialGenerator()


def send_posts(url, location):
    global user_agent, credential_generator
    while True:
        email, password = credential_generator.get_credentials()
        data = {
            "a": email,
            "az": password
        }
        headers = {
            'User-Agent': user_agent.random
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                logger.error(f'{response.status_code} [::] Error sending message. Payload: <{email}> \"{password}\"')
                logger.error(response.text)
                return # kill thread
            logger.info(f'{response.status_code} [::] Sent! Credentials: <{email}> \"{password}\"')
        except Exception as e:
            logger.error('[ERROR] Error sending request!', e)
            return # kill thread


def main():
    global MAX_THREADS, credential_generator
    print(f'{"="*20} phishkiller by CybrZone {"="*20}')
    print()
    print("Enter the URL of the target you want to flood!")
    URL = input('#> ')
    print()
    threads = []
    locations = ["en_US", "en_GB", "it_IT", "en_IE"]

    print('Starting generator thread...')
    t = threading.Thread(target=credential_generator.buffered_generator)
    t.daemon = True
    t.start()

    print(f'Starting phishkiller with {MAX_THREADS} threads...')
    for i in range(1, MAX_THREADS + 1):
        print(f'Starting thread {i}...', end='\r')
        location = random.choice(locations)
        t = threading.Thread(target=send_posts, args=(URL, location))
        t.daemon = True
        threads.append(t)
        t.start()
        print(f'Started thread {i}.{" "*50}', end='\r')
    print('\n\n') # Clear line from \r

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()