import client, micropython, time
from machine import Pin, I2C
import machine

#buffer to store error messages
micropython.alloc_emergency_exception_buf(100)

# Setup the Device Address
deviceAddress = 0x68
playerNum = 1

def callback(pin):
    #schedule to call sensor read function
    micropython.schedule(client_board.read_sensor_reg, 0)

# Initialise the client and the buffer for the registers
client_board = client.Client(playerNum, deviceAddress, 20)

# Declare and setup the interupt pin from the MPU when a new set of values are ready.
p13 = Pin(13, Pin.IN, Pin.PULL_UP)
p13.irq(trigger=Pin.IRQ_FALLING, handler=callback)

while True:
    client_board.mqttClient.wait_msg()
