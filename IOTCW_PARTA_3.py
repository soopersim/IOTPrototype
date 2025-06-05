

# Filename: IOTCW_PARTA_3.py
import machine
import time
from machine import Pin
import network
import urequests
import json
import gc
import random

# Filename: IOTCW_PARTA_3.py
wlan = network.WLAN(network.STA_IF)
board_led=machine.Pin("LED", machine.Pin.OUT)
ssid = ''
password = ''

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyPFMtzUSo-njjHUFHL7NoNnwBNMDM1yxLJZhVOzS0MOkJ5WSRszAGuT9rnXY76CXQm/exec"
TIME_URL = "https://timeapi.io/api/Time/current/zone?timeZone=Europe/London"

def getTime():
    res=urequests.get(url=TIME_URL)
    time=json.loads(res.text)["dateTime"]
    res.close()
    return time

def connectWifi():
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected() and wlan.status() >= 0:
            print("Waiting to connect: ")
            time.sleep(1)
            board_led.off()
        board_led.on()
        print(wlan.ifconfig())
    else:
        print("Wifi already connected...")
        print(getTime())
        
def sendToSpreadsheet(time, sensor1):
    try:
        url=f"{SCRIPT_URL}?time={time}&sensor1={sensor1}"
        
        print(url)
        res=urequests.get(url=url)
        res.close()
        gc.collect()
        
    except NameError:
        print("Error..."+NameError)
        
connectWifi()
wlan.active(True)

for i in range(10):
    timestamp = f"{getTime()}"
    sensor1 = f"{random.randint(0,10)}"
    sendToSpreadsheet(time=timestamp, sensor1=sensor1)
    time.sleep(10)
    
board_led.off()
