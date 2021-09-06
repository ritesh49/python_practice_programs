import traceback
import socket
import codecs

MAX_PACKET = 32768
SERVER_ADDRESS = ('127.0.0.1', 8000)


def recv_all(sock):
    r'''Receive everything from `sock`, until timeout occurs, meaning sender
    is exhausted, return result as string.'''

    # dirty hack to simplify this stuff - you should really use zero timeout,
    # deal with async socket and implement finite automata to handle incoming data

    prev_timeout = sock.gettimeout()
    try:
        sock.settimeout(1)

        rdata = []
        while True:
            try:
                received = sock.recv(MAX_PACKET)
                print('Received Packet')
                print(received)
                try:
                    rdata.append(received.decode())
                except UnicodeDecodeError:
                    # codecs.decode(received, 'hex')
                    rdata.append(codecs.decode(received, 'hex'))
            except UnicodeDecodeError:
                print('Cannot Decode the Packet!!!')
                return ''
            except socket.timeout:
                print('Socket Timeout Error!!!')
                return ''.join(rdata)
            except Exception as e:
                print('Error Occured while receiving packet')
                error = traceback.format_exc()
                print('ERROR ######', error)
                return ''

        # unreachable
    finally:
        sock.settimeout(prev_timeout)


def normalize_line_endings(s):
    r'''Convert string containing various line endings like \n, \r or \r\n,
    to uniform \n.'''
    print('############ Received Message #########')
    print(s)
    return ''.join((line + '\n') for line in s.splitlines())


def run():
    r'''Main loop'''

    # Create TCP socket listening on 10000 port for all connections, 
    # with connection queue of length 1
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server_sock.bind(SERVER_ADDRESS)
    server_sock.listen(1)
    # wrapper = ssl.wrap_socket(server_sock)
    # wrapper.connect(addr)
    print('SSL server accepting connections at 127.0.0.1:8000"')
    try:
        while True:
            # accept connection
            client_sock, client_addr = server_sock.accept()

            # headers and body are divided with \n\n (or \r\n\r\n - that's why we
            # normalize endings). In real application usage, you should handle
            # all variations of line endings not to screw request body
            request = normalize_line_endings(recv_all(client_sock))  # hack again
            print('###### REQUEST RECEIVED SPLITLINES #######')
            print(request)
            if '\n\n' not in request:
                continue
            request_head, request_body = request.split('\n\n', 1)

            # first line is request headline, and others are headers
            request_head = request_head.splitlines()
            request_headline = request_head[0]
            # headers have their name up to first ': '. In real world uses, they
            # could duplicate, and dict drops duplicates by default, so
            # be aware of this.
            request_headers = dict(x.split(': ', 1) for x in request_head[1:])

            # headline has form of "POST /can/i/haz/requests HTTP/1.0"
            request_method, request_uri, request_proto = request_headline.split(' ', 3)
            print('request_method => ', request_method, 'request_uri ==>', request_uri, 'request_proto ==>',
                  request_proto)

            response_body = [
                '<html><body><h1>Hello, world!</h1>',
                '<p>This page is in location %(request_uri)r, was requested ' % locals(),
                'using %(request_method)r, and with %(request_proto)r.</p>' % locals(),
                '<p>Request body is %(request_body)r</p>' % locals(),
                '<p>Actual set of headers received:</p>',
                '<ul>',
            ]

            for request_header_name, request_header_value in request_headers.items():
                response_body.append('<li><b>%r</b> == %r</li>' % (request_header_name, request_header_value))

            response_body.append('</ul></body></html>')
            print('####### RESPONSE BODY #######')
            print(response_body)
            response_body_raw = ''.join(response_body)

            # Clearly state that connection will be closed after this response,
            # and specify length of response body
            response_headers = {
                'Content-Type': 'text/html; encoding=utf8',
                'server': 'Ritesh Ramchandani Server 1.0.0',
                'Content-Length': len(response_body_raw),
                'Connection': 'close',
            }

            response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                           response_headers.items())

            # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
            response_proto = 'HTTP/1.1'
            response_status = '200'
            response_status_text = 'OK'  # this can be random

            # sending all this stuff
            s = '%s %s %s' % (response_proto, response_status, response_status_text)
            print('#### SENDING RESPONSE TO CLIENT #####')
            print('s ==>', s)
            response = f'''
            {s}
            {response_headers_raw}
            {response_body_raw}
            '''.replace('  ', '')
            print('Response to be sent!!!!')
            print(response)
            # client_sock.send(s.encode())
            # print('response_headers ===>', response_headers_raw)
            # client_sock.send(response_headers_raw.encode())
            # client_sock.send('\n'.encode())  # to separate headers from body
            # print('response_body ', response_body)
            client_sock.send(response.encode())

            # and closing connection, as we stated before
            client_sock.close()
    except Exception as e:
        error = traceback.format_exc()
        print(error)
        print('CLOSING HTTP SERVER', e)
        server_sock.close()


run()
