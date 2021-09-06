#!/usr/local/bin/python

import sys
import traceback
import os
import smtpd
import asyncore
import logging
import time
import datetime
import email.utils
import signal
import platform

HOSTNAME = platform.node()

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

logging.basicConfig(stream=sys.stderr,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# os.chdir(os.getenv('MOCK_SMTP_PATH', '.'))
os.chdir('/Users/ritesh/Desktop/microservices_work/kafka_poc/docker_poc/testing/emails')

class MockSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        logging.debug(f'Processing Message with parameters received peer {peer} mailfrom {mailfrom} rcpttos {rcpttos} data {data} kwargs {kwargs}')

        today = time.time()

        rfc822_date = email.utils.formatdate(today, True)

        file = '%s.eml' % datetime.datetime.fromtimestamp(today).strftime('%Y-%m-%dT%T.%f')

        mail = open(file, "w")
        mail.write('Return-Path: <%s>\n' % mailfrom)
        mail.write('Received: from [%s] by %s\n'
                   ' (Mock SMTP -- https://github.com/flaviovs/mock-smtp) with SMTP\n'
                   ' id %s\n'
                   ' for <%s>; %s\n' % (peer[0], HOSTNAME, file,
                                        rcpttos[0], rfc822_date))

        for to in rcpttos:
            mail.write('Envelope-To: <%s>\n' % to)
        mail.write('Delivery-Date: %s\n' % rfc822_date)

        in_header = True
        str_data = data.decode('utf-8')
        for line in str_data.splitlines():
            if in_header and ':' not in line:
                mail.write('\n')
            in_header = False
            mail.write('%s\n' % line)

        mail.close()

        logging.info('%s => %s: %s', mailfrom, rcpttos, file)


def handle_signal(signalnum, frame):
    if signalnum == signal.SIGTERM:
        raise asyncore.ExitNow('SIGTERM')


logging.info('Starting up Mock SMTP server')

# SMTP_HOST = os.getenv('MOCK_SMTP_ADDRESS', '127.0.0.1')
# SERVER_PORT = os.getenv('MOCK_SMTP_PORT', '25')
SMTP_HOST = '127.0.0.1'
SERVER_PORT = 8025
logging.debug(f'Server Running on Host {SMTP_HOST} and port {SERVER_PORT}')
logging.debug(os.getcwd())

smtp_server = MockSMTPServer((SMTP_HOST,
                              int(SERVER_PORT)),
                             None)

if os.getuid() == 0:
    # Switch to UID/GID of owner of current path.
    stat = os.stat('.')
    os.setgroups([])

    os.setgid(stat.st_uid)
    os.setuid(stat.st_gid)
    os.umask(0o77)

# Install signal handler, for handling SIGTERM.
signal.signal(signal.SIGTERM, handle_signal)

# Start the server
try:
    asyncore.loop()
except (KeyboardInterrupt, asyncore.ExitNow):
    pass
except Exception as ex:
    error = traceback.format_exc()
    print(error)

smtp_server.close()