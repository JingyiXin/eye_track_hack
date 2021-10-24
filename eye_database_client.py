import requests


driver1 = {"username": "Dave", "time_blinking": 1, "too_sleepy": False}
r = requests.post("http://127.0.0.1:5000/new_user", json=driver1)
print(r.status_code)
print(r.text)

name = "Betty"
r = requests.get("http://127.0.0.1:5000/blink", json=name)
print(r.status_code)
print(r.text)