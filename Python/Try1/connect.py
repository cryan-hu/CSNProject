import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.35', 9050))
connection, client_address = server_socket.accept()
connection.close()
