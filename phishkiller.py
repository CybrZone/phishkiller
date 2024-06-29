# github.com/lhwe 

import os
from datetime import datetime
from colorama import Fore
import threading
import requests
import random
import string

current_user = os.getenv('USERNAME') or os.getenv('USER')
tlds = ["academy", "accountant", "actor", "agency", "apartments", "associates", "attorney", "auction", "audio", "band", "bar", "bargains", "beer", "best", "bid", "bike", "bingo", "bio", "black", "blackfriday", "blog", "blue", "boutique", "builders", "business", "buzz", "cab", "cafe", "camera", "camp", "capital", "cards", "care", "careers", "cars", "casa", "cash", "casino", "catering", "center", "chat", "cheap", "church", "city", "claims", "cleaning", "click", "clinic", "clothing", "cloud", "club", "coach", "codes", "coffee", "community", "company", "computer", "condos", "construction", "consulting", "contractors", "cooking", "cool", "country", "coupons", "courses", "credit", "creditcard", "cruises", "dance", "date", "dating", "deals", "degree", "delivery", "democrat", "dental", "dentist", "design", "diamonds", "diet", "digital", "direct", "directory", "discount", "domains", "education", "email", "energy", "engineer", "engineering", "enterprises", "equipment", "estate", "events", "exchange", "expert", "exposed", "express", "fail", "faith", "family", "fan", "farm", "fashion", "finance", "financial", "fish", "fishing", "fitness", "flights", "florist", "football", "forsale", "foundation", "fund", "furniture", "futbol", "fyi", "gallery", "games", "garden", "gift", "gifts", "gives", "glass", "global", "gold", "golf", "graphics", "green", "group", "guide", "guru", "healthcare", "help", "hiphop", "hockey", "holdings", "holiday", "horse", "host", "hosting", "house", "ink", "institute", "insure", "international", "investments", "jewelry", "juegos", "kaufen", "kim", "kitchen", "land", "lawyer", "lease", "legal", "lgbt", "life", "lighting", "limited", "limo", "link", "live", "loan", "loans", "lol", "london", "love", "luxury", "maison", "management", "market", "marketing", "mba", "media", "memorial", "men", "menu", "miami", "moda", "moe", "mom", "money", "mortgage", "movie", "music", "network", "news", "ninja", "observer", "one", "online", "ooo", "organic", "partners", "parts", "party", "pet", "pets", "photo", "photography", "photos", "physio", "pics", "pictures", "pink", "pizza", "place", "plumbing", "plus", "poker", "porn", "press", "protection", "pub", "racing", "radio", "realestate", "recipes", "red", "rehab", "reisen", "rent", "rentals", "repair", "report", "republican", "rest", "restaurant", "review", "reviews", "rip", "rocks", "rodeo", "run", "sale", "salon", "sarl", "com", "net", "org", "edu", "gov", "mil", "int", "co.uk", "org.uk", "me.uk", "uk", "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar", "as", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz", "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "cr", "cu", "cv", "cw", "cx", "cy", "cz", "de", "dj", "dk", "dm", "do", "dz", "ec", "ee", "eg", "eh", "er", "es", "et", "eu", "fi", "fj", "fk", "fm", "fo", "fr", "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm", "gn", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy", "hk", "hm", "hn", "hr", "ht", "hu", "id", "ie", "il", "im", "in", "io", "iq", "ir", "is", "it", "je", "jm", "jo", "jp", "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li", "lk", "lr", "ls", "lt", "lu", "lv", "ly", "ma", "mc", "md", "me", "mg", "mh", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt", "mu", "mv", "mw", "mx", "my", "mz", "na", "nc", "ne", "nf", "ng", "ni", "nl", "no", "np", "nr", "nu", "nz", "om", "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", "pr", "ps", "pt", "pw", "py", "qa", "re", "ro", "rs", "ru", "rw", "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl", "sm", "sn", "so", "sr", "ss" "st", "su", "sv", "sx", "sy", "sz", "tc", "td", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to", "tp", "tr","tt", "tv", "tw", "tz", "ua", "ug", "uk", "us", "uy", "uz", "va", "vc", "ve", "vg", "vi", "vn", "vu", "wf", "ws","ye", "yt", "za", "zm", "zw", "biz", "info", "name", "pro", "mobi", "aero", "asia", "cat", "coop", "jobs", "museum", "tel", "travel"]

def generate_random_email():
    local_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(string.ascii_letters + string.digits) + '.' + random.choice(tlds)
    return local_part + '@' + domain

def generate_random_password():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(15))

def read_proxies(filename):
    with open(filename, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

def send_posts(url, proxies):
    while True:
        email = generate_random_email()
        password = generate_random_password()
        data = {
            "a": email,
            "az": password
        }
        try:
            proxy = random.choice(proxies)
            response = requests.post(url, data=data, proxies={'http': proxy, 'https': proxy})
            if response.status_code == 200:
                print(f"{Fore.GREEN}[{datetime.now().strftime('%H:%M:%S')}] Created entry with following data:\nEmail: {email}, Password: {password}, Status Code: {response.status_code}")
            elif response.status_code == 404 or response.status_code == 400:
                print(f'{Fore.RED}[{datetime.now().strftime("%H:%M:%S")}] - Not found, are you sure you put in the correct url?')
            else:
                print(f'{Fore.RED}[{datetime.now().strftime("%H:%M:%S")}] - Response Code: {response.status_code}')
        except Exception as e:
            print(f'{Fore.RED}[{datetime.now().strftime("%H:%M:%S")}] - Error occurred: {str(e)}')

def main():
    os.system("title Phishkiller - by github.com/CybrZone")
    print(f'Welcome to {Fore.CYAN}Phish Killer{Fore.RESET} {current_user}!\nTo get started, please select an option.\n\n')
    menu = Fore.MAGENTA + f"""
    ╔═══╦═══════════════════════╗
    ║ {Fore.BLUE}1{Fore.MAGENTA} ║ Check proxies (soon)  ║
    ╠═══╬═══════════════════════╣
    ║ {Fore.BLUE}2{Fore.MAGENTA} ║ Start {Fore.RED}Phishkiller{Fore.MAGENTA}     ║
    ╚═══╩═══════════════════════╝{Fore.YELLOW}
    """
    print(menu)
    option = input("    > ")
    if option == '1':
        print('Coming soon.')
        proxies = read_proxies('proxies.txt')
        print(f'{len(proxies)} proxies in proxy file.')
    
    elif option == '2':
        print('Starting Phishkiller...')
        os.system('cls' if os.name == 'nt' else 'clear')
        url = input("URL > ").strip()
        
        proxies = read_proxies('proxies.txt')
        threads = []
        
        for _ in range(1500):
            t = threading.Thread(target=send_posts, args=(url, proxies))
            t.daemon = True
            threads.append(t)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
    
    else:
        print('Invalid option!')

if __name__ == "__main__":
    main()
