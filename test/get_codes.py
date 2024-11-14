import requests
code = "GdvEplSJ9FFYe8KkvhtZQQwATYGUyTU6u58e2MOrrU8VTJZOEw"
response = requests.get(url = f"http://127.0.0.1:5000/getviapass?pu_code={code}")
print(response.status_code)
print(response.json)