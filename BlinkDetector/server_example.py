import socket
import struct

rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rec_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rec_sock.bind(("localhost", 1234))

while True:
    data = rec_sock.recv(4096)
    (value,) = struct.unpack_from('<d', data)
    print(f"Received: {value}")