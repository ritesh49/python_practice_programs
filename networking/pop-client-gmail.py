import poplib
import string
# from plone import rfc822
from email import message_from_file
from io import StringIO
import logging

SERVER = "imap.gmail.com"
USER = "faqritesh@gmail.com"
PASSWORD = "Ritesh#4149"

# connect to server
print('connecting to ' + SERVER)
server = poplib.POP3_SSL(SERVER)
# server = poplib.POP3(SERVER)

# login
print('logging in')
server.user(USER)
server.pass_(PASSWORD)

# list items on server
print('listing emails')
resp, items, octets = server.list()

# download the first message in the list
print(f'Message From Servera are ===> resp {resp} items {items} octets {octets}')
for item in items:
    id, size = item.decode().split()
    resp, text, octets = server.retr(id)

    print(f'resp {resp} text {text} octets {octets}')

    # convert list to Message object
    text = b'\n'.join(text).decode()
    file = StringIO(text)
    message = message_from_file(file)
    print('text ------------------------------------- ', message)

    # output message
    print(message['From']),
    print(message['Subject']),
    print(message['Date']),
    #print(message.fp.read())
else:
    print('No More Mails to Fetch from IMAP server')