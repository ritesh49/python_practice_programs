from socket import *

SERVER_PORT = 12000
SERVER_NAME = '0.0.0.0'
MAX_QUEUE_CONNECTION = 1

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_NAME, SERVER_PORT))
server_socket.listen(MAX_QUEUE_CONNECTION)
print(f'########## SERVER LISTENING AT {SERVER_NAME}:{SERVER_PORT} - TCP ##########')

while 1:
    connection_socket, addr = server_socket.accept()
    print('Connection Socket, Address', connection_socket, addr)
    sentence = connection_socket.recv(1024)
    print('Received sentence ==>', sentence)
    capitalized_sentence = sentence.upper()
    print('Modified sentence ==>', capitalized_sentence)
    connection_socket.send(capitalized_sentence)
    connection_socket.close()

