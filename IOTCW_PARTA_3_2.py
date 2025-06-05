

# Filename: IOTCW_PARTA_3_2.py
import machine
import time
from machine import Pin, I2C
import network
import urequests
import json
import gc
from bme280 import BME280

wlan = network.WLAN(network.STA_IF)
board_led=machine.Pin("LED", machine.Pin.OUT)
ssid = ''
password = ''

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz01jgcLQbH8llyP_t72-1YUaiUr8IZdL3Q9h6beAYkImSjPhee7r1OryB4zOhTHAB6qQ/exec"
TIME_URL = "https://timeapi.io/api/Time/current/zone?timeZone=Europe/London"

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bme = BME280(i2c=i2c)

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
        
def send_to_sheet(time, temp, pressure, humidity):
    try:
        url = f"{SCRIPT_URL}?time={time}&temp={temp}&pressure={pressure}&humidity={humidity}"
        response = urequests.get(url)
        response.close()
        gc.collect()
    except Exception as e:
        print("Failed to send data:", e)

        
connectWifi()
wlan.active(True)

for i in range(20):
    timestamp = f"{getTime()}"
    temp_str, pressure_str, humidity_str = bme.values
    temp = float(temp_str[:-1]) 
    pressure = float(pressure_str[:-3])
    humidity = float(humidity_str[:-1])
    
    send_to_sheet(timestamp, temp, pressure, humidity)
    print(f"Sent: {timestamp}, {temp}C, {pressure}hPa, {humidity}%")
    time.sleep(15)

board_led.off()
