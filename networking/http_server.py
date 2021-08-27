from socket import *

SERVER_PORT = 8080
SERVER_NAME = '127.0.0.1'

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(())
