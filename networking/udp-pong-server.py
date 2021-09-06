"""
Networking: Top Down Approach
Chapter 2 WIRESHARK LABS
Assignment 2
Owner: Ritesh Ramchandani
Udp server for pong messages
"""

from socket import *
import json
import time

SERVER_PORT = 12000
SERVER_HOST = '127.0.0.1'

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print('Server is ready to receive some exciting messages!!')

while True:
    message, client_address = server_socket.recvfrom(2048)
    print(f'Received message {message} with client address {client_address}')
    _message = json.loads(message)
    _message['message_type'] = 'pong'
    __message = json.dumps(_message).encode()
    # modified_message = message.upper()
    # print(f'Sending Modified message = {modified_message} to client_address')
    server_socket.sendto(__message, client_address)
