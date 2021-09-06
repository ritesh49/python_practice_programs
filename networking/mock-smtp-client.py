import smtplib

sender = 'riteshramchandani123@gmail.com'
receivers = ['ritesh@hubbler.mobi']

message = f'''
From: {sender}
To: {receivers}
Subject: SMTP e-mail test

This is a test e-mail message.
'''

try:
    smtp_obj = smtplib.SMTP(host='localhost', port=8025)
    smtp_obj.sendmail(sender, receivers, message)
    print('Successfully Send Email')
except smtplib.SMTPException:
    print('Unable to send email')
