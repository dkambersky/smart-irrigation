from network import LoRa
import pycom, socket, time, sys


## Valve controller node code - receives LoRa messages
# Because we don't actually have a valve to control, the state is signalized by the LED color gradient.
# Full red = 0% througput. 
# Yellow  = 50% throughput.
# Green = 100% throughput.
#
# This would obviously need actual motor / valve control outside of the scope of the hackathon.

# Globals
sleep_interval = 5
flow_rate = None



# -------------------------------- Utility functions --------------------------- #
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
EPSILON = 0.0000000002  # smallest possible difference

def convert_to_rgb(minval, maxval, val, colors):
    fi = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i = int(fi)
    f = fi - i
    if f < EPSILON:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))


def intensity_color():
    minval, maxval = 1, 100
    steps = 20
    delta = float(maxval-minval) / steps
    colors = [ (255, 0, 0),(0, 255, 0)]  # [BLUE, GREEN, RED]
    
    val = flow_rate
    r, g, b = convert_to_rgb(minval, maxval, val, colors)
    print('{:.3f} -> ({:3d}, {:3d}, {:3d})'.format(val, r, g, b))

    return getIfromRGB([r,g,b])
    # return rgb_to_hex((r,g,b))


def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    # print red, green, blue
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint



# Setup 
print("Valve controller starting")
pycom.heartbeat(False)
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
pycom.rgbled(0x0055ff)

# Loop
while True:
    recv = s.recv(64)

    
    if recv[:4] == b'Flow':
        flow_rate = int(recv[5:])
        print("Flow command received! " + str(flow_rate))
        color = intensity_color()
        # print("Color" + str(color))
        pycom.rgbled(color)



    # Debug
    # if recv == b'ValveOn':
    #     print('Valve open')\
    #     pycom.rgbled(0x00ff00)
    # elif recv == b'ValveOff':
    #     print('Valve closed')
    #     pycom.rgbled(0xff0000)

    time.sleep(sleep_interval)

