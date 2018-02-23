from network import LoRa
import socket
import machine
from machine import UART
import time
import re
import pycom

pycom.heartbeat(False)

uart = UART(1, baudrate=9600) #setting bus for serial communication

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868) #setting up LoRa transmission
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

adc = machine.ADC() # reading analogue signal from LDR
apin = adc.channel(pin="P16")


while True:
    numOfChar = uart.any()
    if (numOfChar is not None and numOfChar>0):
        val = uart.read(numOfChar) + str(apin())
        print(val)
        if "null" in val:
            s.send("null")
            for i in range(0, 3):
                pycom.rgbled(0xff0000)
                time.sleep(0.2)
                pycom.rgbled(0x000000)
                time.sleep(0.2)
        else:
            s.send(val)
            pycom.rgbled(0x00ff00)
            time.sleep(1)
            pycom.rgbled(0x000000)
