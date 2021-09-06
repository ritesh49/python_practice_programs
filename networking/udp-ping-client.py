"""
Networking: Top Down Approach
Chapter 2 WIRESHARK LABS
Assignment 2
Owner: Ritesh Ramchandani
Udp Client for ping messages
"""

from socket import *
from uuid import uuid4
import json
import time

# client details
# SERVER_NAME = '192.168.29.122'
SERVER_NAME = '127.0.0.1'
SERVER_PORT = 12000

# initiating connecting and sending data
client_socket = socket(AF_INET, SOCK_DGRAM)
get_message_id = lambda: uuid4().__str__()
message = {'message_type': 'ping'}

for i in range(10):
    message['id'] = i
    message['start_time'] = time.time()
    b_message = json.dumps(message).encode()
    client_socket.sendto(b_message, (SERVER_NAME, SERVER_PORT))
    print(f'Message {message} send to', SERVER_NAME, SERVER_PORT, i)

for i in range(10):
    # receiving response message from server
    server_message, _ = client_socket.recvfrom(2048)
    _message = json.loads(server_message)
    print('Received Message!!!', _message, i)
    message_type = _message.get('message_type')

    if message_type == 'pong':
        _message['end_time'] = time.time()
        start_time = _message.get('start_time')
        end_time = _message.get('end_time')
        exec_time = end_time - start_time
        print('Message Execution took ', exec_time, 'milliseconds!!!')
    else:
        print('Invalid MEssage Type ', message_type)

    print('Message Id')
    #

client_socket.close()
