import threading
import requests

url = "https://haquegrp.com/xl/ecc2.php"

data = {
    "a": "fuckyou@fckU.com",
    "az": "RIPBOZO"
}

def send_posts():
    while True:
        response = requests.post(url, data=data)
        print(response.status_code)

threads = []

for i in range(50):
    t = threading.Thread(target=send_posts)
    t.daemon = True
    threads.append(t)

for i in range(50):
    threads[i].start()

for i in range(50):
    threads[i].join()
