from socket import *

# client details
# SERVER_NAME = '192.168.29.122'
SERVER_NAME = '13.212.139.67'
SERVER_PORT = 12000

# initiating connecting and sending data
client_socket = socket(AF_INET, SOCK_DGRAM)
message = 'Hello There Kubernetes Server!!!'.encode('utf-8')
client_socket.sendto(message, (SERVER_NAME, SERVER_PORT))
print(f'MEssage {message} send to', SERVER_NAME, SERVER_PORT)  # server details required for sending UDP packet

# receiving response message from server
modified_message, server_address = client_socket.recvfrom(2048)
print('Server Address is - ', server_address)
print('Modified message ===>', modified_message)
client_socket.close()
