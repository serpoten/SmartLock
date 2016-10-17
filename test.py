from umqtt.simple import MQTTClient
import ulno_iot_devel as devel
from machine import Pin
import ubinascii
import machine
import micropython
import time


# Setting the Relay

d1=Pin(5,Pin.OUT)

def cerrado():
    d1.low()


def open():
    d1.high()


# Default MQTT server to connect to
SERVER = "192.168.1"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = "test/test" # Frist is the topic and then the subtopic 


def sub_cb(topic, msg):
    global state
    
    if msg == b"on":
        devel.blue.low()
	d1.high()
     
    elif msg == b"off":
        devel.blue.high()
	d1.low()
      

def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, server)

    # Subscribed messages will be delivered to this callback

    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

    try:
        while 1:
            #micropython.mem_info()
            c.wait_msg()
    finally:
        c.disconnect()

main()
