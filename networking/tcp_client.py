from socket import *

SERVER_NAME = '13.212.139.67'
SERVER_PORT = 12000

client_socket = socket(AF_INET, SOCK_STREAM)
print(f'Connecting to {SERVER_NAME}:{SERVER_PORT} - TCP')
client_socket.connect((SERVER_NAME, SERVER_PORT))

sentence = """
This is a Test Sentence in a very
particular format of RFC
for sending it to server
""".encode('utf-8')
print('Sending sentence ===>', sentence.decode())
client_socket.send(sentence)  # client didn't attached the server details as with UDP

modified_sentence = client_socket.recv(1024)
print('Receiving modified sentence from server ', modified_sentence.decode())
client_socket.close()
