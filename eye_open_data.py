import socket
import struct
import requests

rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rec_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rec_sock.bind(("localhost", 1234))

while True:
    data = rec_sock.recv(4096)
    (value,) = struct.unpack_from('<d', data)
    print(f"Received: {value}")
    too_sleepy = False
    if value < 0.27:
        too_sleepy = True
    driver = {"username": "Bob", "time_blinking": value, "too_sleepy": False}
    r = requests.post("http://vcm-23122.vm.duke.edu:5000/new_user",
                      json=driver)
    print(r.status_code)
    print(r.text)