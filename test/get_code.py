import requests

print(requests.post(url = "http://127.0.0.1:5000/send_verify", json = {"username":"lucas@gmail.com"}).text)