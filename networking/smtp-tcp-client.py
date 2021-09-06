from socket import *
# import ssl
from base64 import b64encode as encode

SERVER_BACKEND = 'smtp.gmail.com'
SERVER_PORT = 465
username = encode(b'faqritesh@gmail.com')
password = encode(b'Ritesh#4149')

s = socket(AF_INET, SOCK_STREAM)
print('initiating')
s.connect((SERVER_BACKEND, SERVER_PORT))

print('Sending Helo Message!!!')
s.send(b'HELO mail.gmail.com\r\n')
# print('Sending Starttls Message!!!')
# s.send(b'starttls\r\n')
# print('Wrapping Socket!!!')
# ssl.wrap_socket(s)

print('Authenticating to mail server!!')
s.send(b'auth login\r\n')
s.send(username + b'\r\n')
s.send(password + b'\r\n')
# print('Auth Login Received!!!', s.recv(1024))

s.send(b'MAIL FROM: <faqritesh@gmail.com>\r\n')
s.send(b'RCPT TO: <riteshramchandani123@gmail.com\r\n')
s.send(b'DATA\r\n')

msg = 'FROM: ' + 'faqritesh@gmail.com' + '\r\n'
msg += 'TO: ' + 'riteshramchandani123@gmail.com' + '\r\n'
msg += 'Subject: ' + 'test' +  '\r\n'
msg += "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

s.send(msg.encode())
s.send(endmsg.encode())

s.send(b'QUIT\r\n')

print('Finished!!')

"""
HELO mail.gmail.com
starttls
auth login
ZmFxcml0ZXNoQGdtYWlsLmNvbQ==
Uml0ZXNoIzQxNDk=
MAIL FROM: <faqritesh@gmail.com>
RCPT TO: <riteshramchandani123@gmail.com>
DATA
FROM: faqritesh@gmail.com
TO: riteshramchandani123@gmail.com
CustomHeader: ritesh_ramchandano_smtp_server_1_2
Subject: test
I love computer networks! This is Test message from openssl s_client --connect smtp.gmail.com -quiet

.
QUIT

"""
