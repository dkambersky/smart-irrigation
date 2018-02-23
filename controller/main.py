import socket, time, sys, machine, pycom
from network import LoRa, WLAN

## Central node code:
# - polls sensors
# - sends commands to actuators
# - communicates with cloud server

# LED meanings:
# - Blue: initializing
# - Green: receiving data from sensors
# - Red: transmitting data to actuators
# - Cloudy blue: communicating with cloud Controller
# - Dim blue: sleeping

# Globals
sleep_interval = 5
ledOn = False
lora_socket = None
sensors = {}
flow_rate = None

# Colors
color_dim = 0x00000f
color_recv = 0x00ff00
color_send= 0xff0000
color_cloud = 0x00ffff
flash_length = 0.25


# --------------------------- LoRa Communication ----------------------------- #

def sendToActuators(intensity):
    pycom.rgbled(color_send)

    if not flow_rate == None:
        lora_socket.send('Flow ' + flow_rate)



    # Debug comms
    # global ledOn
    # if ledOn:
    #     lora_socket.send('ValveOn')
    # else:
    #     lora_socket.send('ValveOff')
    #
    # ledOn = not ledOn
    # Debug comms end


    time.sleep(flash_length)
    pycom.rgbled(color_dim)

def receiveFromSensors():
    pycom.rgbled(color_recv)
    msg = lora_socket.recv(100)

    if (not msg == b'null') and (not msg == b''):
        parseSensorMessage(msg)

    time.sleep(flash_length)
    pycom.rgbled(color_dim)


def parseSensorMessage(msg):
    msg = msg.decode('UTF-8')

    global sensors
    sensors['temperature'] = int(float(msg[0:5]))
    sensors['humidity'] = int(float(msg[7:12]))
    sensors['light'] = msg[16:]

    print(sensors)


# --------------------------- Wi-Fi and HTTP  ----------------------------- #
def connectToWifi():
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'NSA SURVEILLANCE TRUCK 3':
            print('Network found!')
            wlan.connect(net.ssid, auth=(net.sec, 'connect me please 2'), timeout=5000)
            while not wlan.isconnected():
                machine.idle() # save power while waiting

            print('WLAN connection succeeded!')
            break



def connectCentral():
    wlan = WLAN(mode=WLAN.STA)
    print("Please enter your UUN")
    uun =  sys.stdin.readline()[0:-1]
    email ='uun + @ed.ac.uk'
    print ("Please enter your password")
    creds = sys.stdin.readline()[0:-1]
    while not(wlan.isconnected()):
        wlan.connect(ssid='NSA SURVEILLANCE TRUCK 3', auth=(WLAN.WPA2_ENT, 'connect me please'), timeout=5000)
        time.sleep(5)
    print ('WiFi Connected')

# Working
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


# Working
def http_post(url, data):
    _, _, host, path = url.split('/', 3)
    port = 80
    POST_DATA = str(data)

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

    response = b''
    while True:
        data = s.recv(100)
        if data:
            response = response + data
        else:
            break
    s.close()

    # Parse the response, get flow rate, save it to the Globals
    global flow_rate
    flow_rate = response.decode('UTF-8').split("\r\n\r\n")[1]
    print("Flow rate: " + flow_rate)



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


def communicateWithCloud():
    pycom.rgbled(color_cloud)
    global sensors
    msg = str(sensors['temperature']) + " " +str(sensors['humidity']) + " " +sensors['light'] + " -1"
    http_post('http://flaskserver.azurewebsites.net/get_flow_rate', msg)

    time.sleep(flash_length)
    pycom.rgbled(color_cloud)


# --------------------------- LoPy node behavior ----------------------------- #

# Heartbeat step
def heartbeatStep():
    sendToActuators(5)
    time.sleep(sleep_interval/2)
    receiveFromSensors()
    time.sleep(sleep_interval/2)
    communicateWithCloud()
    time.sleep(sleep_interval/2)


def initialize():
    print("Controller node starting")
    pycom.heartbeat(False)
    # Boot LED
    pycom.rgbled(0x0055ff)

    # Initialize LoRa
    lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
    global lora_socket
    lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    lora_socket.setblocking(False)
    ledOn = False

    # Initialize WiFi
    connectToWifi()

    pycom.rgbled(color_dim)


# ----- THE BELOW CODE RUNS ON BOOT ----- #

# Initialize
initialize()

# Loop
while True:
    heartbeatStep()
    # time.sleep(sleep_interval)
