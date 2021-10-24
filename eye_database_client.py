import requests


driver1 = {"username": "Dave", "time_blinking": 1, "too_sleepy": False}
r = requests.post("http://vcm-23122.vm.duke.edu/new_user", json=driver1)
print(r.status_code)
print(r.text)

name = "Betty"
r = requests.get("http://vcm-23122.vm.duke.edu/blink", json=name)
print(r.status_code)
print(r.text)