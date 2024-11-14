import requests

public_code = "GdvEplSJ9FFYe8KkvhtZQQwATYGUyTU6u58e2MOrrU8VTJZOEw"
private_code = "s0ufC6Syv3NQT1Q0dY2qSQfUF4H5ufDxo97gCrACqGnZY1vfdm"
username = "lucas@gmail.com"
password = "Imbecil44&&"
response = requests.post(url = "http://127.0.0.1:5000/registration", json = {"pu_code": public_code, "pr_code": private_code, "username": username, "password":password, "repassword": password})
print(response.text, response.status_code)