

# Filename: IOTCW_PARTA_1.py
import machine
from machine import Pin, I2C
import time
import bme280

i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

bme = bme280.BME280(i2c=i2c)

try:
    while True:
        temp = bme.values[0]
        pressure = bme.values[1]
        humidity = bme.values[2]
       
        print(f"Temperature: {temp}, Pressure: {pressure}, Humidity: {humidity}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Program terminated by user.")
