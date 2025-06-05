

# Filename: IOTCW_PARTB_2.py

import machine
import time
from machine import Pin, I2C
import network
import urequests
import json
import gc
from bme280 import BME280

wlan = network.WLAN(network.STA_IF)
board_led = Pin("LED", Pin.OUT)
ssid = ''
password = ''
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby-2CpE6IqHPGf2Af9kLZffPvgU4mABoKr05KISQ1Mlh0AjgQkn6FgiHKbgaoyHTw/exec"
TIME_URL = "https://timeapi.io/api/Time/current/zone?timeZone=Europe/London"

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bme = BME280(i2c=i2c)

def get_time():
    try:
        response = urequests.get(TIME_URL, timeout=5)
        time_str = json.loads(response.text)["dateTime"]
        response.close()
        return time_str
    except Exception as e:
        print("TimeAPI Error:", e)
        return None

def connect_wifi():
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print("Connecting to WiFi...")
            time.sleep(2)
            board_led.off()
        board_led.on()
        print("Connected. IP:", wlan.ifconfig()[0])

def send_to_sheet(time, temp):
    try:
        url = f"{SCRIPT_URL}?time={time}&temp={temp}"
        response = urequests.get(url, timeout=10)
        print("Response:", response.text)
        response.close()
        gc.collect()
        return True
    except Exception as e:
        print("Send Error:", e)
        gc.collect()
        return False

connect_wifi()

for _ in range(20):
    current_time = get_time()
    if not current_time:
        print("Failed to fetch time. Retrying...")
        time.sleep(5)
        continue
    
    temp_str, _, _ = bme.values
    temp = float(temp_str[:-1]) 
    
    success = send_to_sheet(current_time, temp)
    if success:
        print(f"Sent: {current_time}, {temp}°C")
    else:
        print("Retrying...")
        time.sleep(10)
    
    time.sleep(15) 

board_led.off()
