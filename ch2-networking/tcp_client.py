import socket

target_host = "192.168.29.209"   # the SERVER laptop's WiFi IP
target_port = 9998

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
client.send(b"Hello from the client laptop")   # client sends first
response = client.recv(4096)                    # wait for the server's reply
print(response.decode())                         # should print: ACK
client.close()
