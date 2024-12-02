import socket

server_name = "Server Name"
server_port = 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, server_port))
sentence = raw_input("Input lowercase sentence:")
client_socket.send(sentence.encode())
modified_sentence = client_socket.recv(1024)
print("From Server: ", modified_sentence.decode())
client_socket.close()