# SmartLock
Project for Home & Building Automation Course


Most of the code has been taken from other Git repositories.

In order to be able to run the provided code you will need,

 - Install the python-devel package into the Raspberry : sudo apt-get install python2.7-dev

 - Install the SPI module in order to be able to communicate the NFC reader with the Pi : https://github.com/lthiery/SPI-Py

 - Install the NFC[MFRC522] module into the PI.: https://github.com/mxgxw/MFRC522-python

 - Have in the same file the NFC module and the smart.py 

 - Install MQTT into the pi via paho: https://pypi.python.org/pypi/paho-mqtt/1.1

 - MQTT for Micro: https://github.com/micropython/micropython-lib/tree/master/umqtt.simple

 - For the Shields & Micropython ESP8266 please reed the documentation from ULNO : https://github.com/ulno/micropython-extra-ulno 
