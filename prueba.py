!/usr/bin/env python
# -*- coding: utf8 -*-
# Credit to mxgxw whose program this is based on

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

sergio = '2535271213'# White card
lockcard = '1119146248' #My Fh card
tag = '11821512565' #Blue Tag
card = '11111111111'

#Initial condition of the Lock card = Closed

locked= '1'

#GPIO setup

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
        statusFile2 = open('/home/pi/status2.txt', 'r')
        openTrigSwitch = statusFile2.readline()
        statusFile2.close()

        if UIDcode == sergio:
            adminpriv = 1
        else:
            adminpriv = 0

        if UIDcode == sergio or UIDcode == tag or UIDcode == card:
            if locked == '0' or adminpriv == 1:
		GPIO.setup(12, GPIO.OUT)
		# Yelloe LED ON
		GPIO.output(12,GPIO.HIGH)
				
		# MQTT send OPEN= "on"
		mqttc.publish("test/test", "on")
				
		print "Door open"				
		time.sleep(3) 
				
                print "Finished"
				
		# Yellow LED OFF
		GPIO.output(12,GPIO.LOW)
            else:
                print "Door locked"
		# RED Blinking = Door LOCKED
		GPIO.setup(16, GPIO.OUT)
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
            if locked == '0':
			
		GPIO.setup(12, GPIO.OUT)
		time.sleep(0.05)
		GPIO.output(12,GPIO.HIGH)
		time.sleep(0.05)
		GPIO.output(12,GPIO.LOW)
		#counter = counter + 1
		locked = '1'
		time.sleep(1)
				
            else:
			
		GPIO.setup(12, GPIO.OUT)
		time.sleep(0.05)
		GPIO.output(12,GPIO.HIGH)
		time.sleep(0.05)
		GPIO.output(12,GPIO.LOW)
		#counter = counter + 1
		locked = '0'
		time.sleep(1)

            fh = open('status.txt', 'w')
            fh.write(str(locked))
            fh.close()

        else:
		print "Unrecognised Card"
		# RED Blinking = Door CLOSED
		GPIO.setup(16, GPIO.OUT)
		GPIO.output(16,GPIO.HIGH)
		time.sleep(5)
				
		# MQTT send OPEN= "off"
		mqttc.publish("test/test", "off")
