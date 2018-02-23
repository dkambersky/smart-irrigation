import socket

# working
def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data))
        else:
            break
    s.close()


# working
def http_post(url):
    _, _, host, path = url.split('/', 3)
    port = 80
    POST_DATA = "1 2 3 4"

    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)

    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect((HOST,port))
    # s.send(bytes('POST / HTTP/1.1\r\n', 'utf8'))
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n' % (path, host), 'utf8'))
    # s.send(bytes('Host: ' + host + '\r\n', 'utf8'))
    s.send(bytes('Connection: KeepAlive\r\n', 'utf8'))
    s.send(bytes('Content-Type: text/plain\r\n', 'utf8'))
    s.send(bytes('Content-Length: ' + str(len(POST_DATA)) + '\r\n', 'utf8'))
    s.send(bytes('\r\n', 'utf8'))
    s.send(bytes(POST_DATA, 'utf8'))

    number = None
    while True:
        data = s.recv(100)
        if data:
            number = str(data)[-3:-1]
        else:
            break
    print(number)
    s.close()



"""this also works"""
    # stream = s.makefile()
    # responseLength = 0
    #
    # # Read Header
    # while True:
    #     data = stream.readline()
    #     if data.startswith('Content-Length'):
    #         responseLength = data.split(' ')[1]
    #     print(data)
    #     if data == '\r\n':
    #         break
    #
    # print("responseLength is " + str(responseLength))
    #
    # # Read Body
    # response = ''
    # for i in range(0, int(responseLength)):
    #      response = response + stream.read(1)
    #
    # print(response)
    #
    # s.close()

http_post('http://flaskserver.azurewebsites.net/hello')
# http_post('http://httpbin.org/post')
