#!/usr/bin/env python
# -*- coding: utf8 -*-
# Credit to mxgxw and cameronkempster whose program this is based on  

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import paho.mqtt.client as mqtt

# set up the mqtt client
mqttc = mqtt.Client("NFC-READER")
 
 # the server to publish to, and corresponding port
mqttc.connect("10.0.0.102", 1883)
 
# GPIO Mode

GPIO.setmode(GPIO.BOARD) 

# Card Register

sergio = '0000'# White card
lockcard = '0000' #My Master Card
tag = '0000' #Blue Tag
card = '0000'

#Initial condition of the Lock card = Closed

var = 0

#GPIO setup

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# Initialise the Script

print "Welcome to your SmartLock Nfc"

continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

while continue_reading:

# Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        UIDcode = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        print UIDcode

        # Control door lock
        statusFile = open('/home/pi/status.txt', 'r')
        locked = statusFile.readline()
        statusFile.close()
        

        if UIDcode == sergio:
            adminpriv = 1
	    var = 1

        else:
            adminpriv = 0

        if UIDcode == sergio or UIDcode == tag or UIDcode == card:
            if locked == '0' or adminpriv == 1 or var == 0:
		
		# Yelloe LED ON
		GPIO.output(12,GPIO.HIGH)
				
		# MQTT send OPEN= "on"
		mqttc.publish("test/test", "on")
				
		print "Door open"				
		time.sleep(4) # Opens the door 4 seconds
				
                print "Finished"
				
		# Yellow LED OFF
		GPIO.output(12,GPIO.LOW)
            else:
                print "Door locked"
		# RED Blinking = Door LOCKED
		GPIO.output(16,GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(16,GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(16,GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(16,GPIO.LOW)
		time.sleep(0.5)
		# MQTT send OPEN= "off"
		mqttc.publish("test/test", "off")
				
				
        elif UIDcode == lockcard:
            counter = 0
            if locked == '0' or var == 0:
			
		GPIO.output(12,GPIO.HIGH)
		time.sleep(0.05)
		GPIO.output(12,GPIO.LOW)
		#counter = counter + 1
		locked = '1'
		var = 1
		print "Chanded to Opened"
		time.sleep(1)
				
            else:
			
		GPIO.output(12,GPIO.HIGH)
		time.sleep(0.05)
		GPIO.output(12,GPIO.LOW)
		#counter = counter + 1
		locked = '0'
		var = 0
		print "Changed to Closed"
		time.sleep(1)

            fh = open('status.txt', 'w')
            fh.write(str(locked))
            fh.close()

        else:
		print "Unrecognised Card"
		# RED Blinking = Door CLOSED
		GPIO.output(16,GPIO.HIGH)
		time.sleep(5)
		GPIO.output(16,GPIO.LOW)		
		# MQTT send OPEN= "off"
		mqttc.publish("test/test", "off")
