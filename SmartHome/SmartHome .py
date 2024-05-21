from machine import SoftI2C, Pin, Timer, ADC
import random
import utime
import HTU21D
import ssd1306
from mq9 import MQ9
import time
from PIRsensor import PIRSensor
from FlameSensor import FlameSensor
import network
import espnow
import ujson

############################### ESP-NOW PART ##########################################

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xb0\xa72+\xbd\xc4'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

DEVICE_ID = 'SmartHome'

############################### OLED PART ##########################################

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.invert(False)


############################### MQ9 PART ##########################################

# Define pin numbers
analog_pin = 32  # Analog pin A0 on ESP32
digital_pin = 25   # Digital pin D2 on ESP32

# Initialize the MQ-9 sensor
mq9_sensor = MQ9(analog_pin, digital_pin)

############################### PIR PART ##########################################

pir_sensor_pin = 19  # GPIO pin connected to the PIR sensor
pir_sensor = PIRSensor(pir_sensor_pin)


############################### FLAMESENSOR PART ##########################################

flame_sensor = FlameSensor(analog_pin=33, digital_pin=5)

############################### TIMERS PART ##########################################

def timer0_handler(t):
    lectura = HTU21D.HTU21D(22,21)
    hum = lectura.humidity
    temp = lectura.temperature
    co_gas, smoke_gas, lpg_gas = mq9_sensor.read_gas_concentration()
    
    #print('Humidity:\n ', + hum)
    #print('Temperature:\n ', + temp)
    #print("CO gas concentration:", co_gas, "ppm")
    #print("Smoke gas concentration:", smoke_gas, "ppm")
    #print("LPG gas concentration:", lpg_gas, "ppm")
    #print("\n")

    
def timer1_handler(t):
    lectura = HTU21D.HTU21D(22,21)
    hum = round(lectura.humidity)
    temp = round(lectura.temperature)
    temperature_string = str(temp)
    humidity_string = str(hum)
    
    co_gas, smoke_gas, lpg_gas = mq9_sensor.read_gas_concentration()
    co_gas_round = round(co_gas)
    co_gas_round_string = str(co_gas_round)
    
    oled.text("Temperature: ", 0, 20)
    oled.text(temperature_string, 100, 20)
    
    oled.text("Humidity: ", 0, 30)
    oled.text(humidity_string, 100, 30)
    
    oled.text("CO gas: ", 0, 40)
    oled.text(co_gas_round_string, 100, 40)
    
    oled.show()
    oled.fill(0)


def timer2_handler(t):
    
    if pir_sensor.check_motion():
        print("Motion detected!")

    flame_sensor.read_sensor()


def send_data(t):
    
    lectura = HTU21D.HTU21D(22,21)
    hum = lectura.humidity
    temp = lectura.temperature

    co_gas, smoke_gas, lpg_gas = mq9_sensor.read_gas_concentration()
    motion_detected = pir_sensor.check_motion()
    flame_detected = flame_sensor.read_sensor()

    data = {
        'device_id': DEVICE_ID,
        'temperature': temp,
        'humidity': hum,
        'co_gas': co_gas,
        'smoke_gas': smoke_gas,
        'lpg_gas': lpg_gas,
        }

    # Add motion detection info if motion is detected
    if pir_sensor.check_motion():
        data['motion_detected'] = True

    # Add flame detection info if flame is detected
    if flame_sensor.read_sensor():
        data['flame_detected'] = True


    json_data = ujson.dumps(data)
    e.send(peer, json_data)


timer0 = Timer(0)
timer1 = Timer(1)
timer2 = Timer(2)
timer3 = Timer(3)


timer0.init(period= 5000, mode=Timer.PERIODIC, callback=timer0_handler)
timer1.init(period= 2000, mode =Timer.PERIODIC, callback=timer1_handler)
timer2.init(period= 1000, mode =Timer.PERIODIC, callback=timer2_handler)
timer3.init(period= 1000, mode =Timer.PERIODIC, callback=send_data)

















