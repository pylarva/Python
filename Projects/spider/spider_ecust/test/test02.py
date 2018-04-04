import socket

sk = socket.socket()
sk.connect(('115.239.210.27', 80))

sk.sendall(bytes('111', encoding='utf-8'))
recv_bytes = sk.recv(1024)
recv_str = str(recv_bytes, encoding='utf-8')
print(recv_str)