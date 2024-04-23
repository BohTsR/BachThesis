# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


from machine import I2C, Pin
import time

# HTU21D I2C address
HTU21D_I2C_ADDR = 0x40

# Commands
HTU21D_TRIGGER_TEMP_MEASURE_HOLD = 0xE3
HTU21D_TRIGGER_HUMD_MEASURE_HOLD = 0xE5
HTU21D_TRIGGER_TEMP_MEASURE_NOHOLD = 0xF3
HTU21D_TRIGGER_HUMD_MEASURE_NOHOLD = 0xF5

# Coefficients
HTU21D_TEMPERATURE_COEFFICIENT = -46.85
HTU21D_HUMIDITY_COEFFICIENT = -6.0

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

def read_sensor(command):
    i2c.writeto(HTU21D_I2C_ADDR, bytearray([command]))
    time.sleep_ms(50)
    data = i2c.readfrom(HTU21D_I2C_ADDR, 2)
    value = (data[0] << 8) + data[1]
    return value

def read_temperature():
    value = read_sensor(HTU21D_TRIGGER_TEMP_MEASURE_NOHOLD)
    temperature = value * 175.72 / 65536 - 46.85
    return temperature

def read_humidity():
    value = read_sensor(HTU21D_TRIGGER_HUMD_MEASURE_NOHOLD)
    humidity = value * 125 / 65536 - 6
    return humidity

import network
import espnow
import time 
 
 # A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266
 
e = espnow.ESPNow()
e.active(True)
peer = b'\xb0\xa72+\xbd\xc4'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()


temperature = read_temperature()
humidity = read_humidity()

temperature = int(temperature * 100)

print('Humidity:\n ', + humidity)
print('Temperature:\n ', + temperature/100)

while True:
    temperature = read_temperature()
    humidity = read_humidity()
    e.send(peer, bytes([int(temperature*100)]))
    e.send(peer, bytes([int(humidity*100)]))
    time.sleep(5)
