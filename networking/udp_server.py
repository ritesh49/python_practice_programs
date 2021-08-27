from socket import *

SERVER_PORT = 12000
SERVER_HOST = '192.168.29.122'

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print('Server is ready to receive some exciting messages!!')

while True:
    message, client_address = server_socket.recvfrom(2048)
    print(f'Received message {message} with client address {client_address}')
    modified_message = message.upper()
    print(f'Sending Modified message = {modified_message} to client_address')
    server_socket.sendto(modified_message, client_address)
