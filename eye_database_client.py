import requests


driver1 = {"username": "Bob", "time_blinking": 2, "too_sleepy": False}
r = requests.post("http://vcm-23122.vm.duke.edu:5000/new_user", json=driver1)
print(r.status_code)
print(r.text)

name = "Betty"
r = requests.get("http://vcm-23122.vm.duke.edu:5000/sleepy", json=name)
print(r.status_code)
print(r.text)