# Student name: Simranjit Kaur Gill
# Student ID: W19314851

# Filename: IOTCW_PARTA_2.py
import machine
from machine import Pin, I2C
import network
import socket
import time
import bme280

ssid = 'sim'
password = 'lofiish-0'

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c)

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(reading):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Pico W BME280 Sensor</title>
    <meta http-equiv="refresh" content="10">
    </head>
    <body>
    <h1>BME280 Sensor Readings</h1>
    <p>{reading}</p>
    </body>
    </html>
    """
    return str(html)

def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
       
        temp = bme.values[0]
        pressure = bme.values[1]
        humidity = bme.values[2]
       
        reading = f"Temperature: {temp}, Pressure: {pressure}, Humidity: {humidity}"
        html = webpage(reading)
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()