import requests

flag = True

url = ''


data = {}


while flag:
response = requests.post(url, data=data)

print(response.status_code)
