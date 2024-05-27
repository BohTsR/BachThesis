# Import necessary modules and libraries
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

# Initialize WLAN interface for ESP-NOW communication
sta = network.WLAN(network.STA_IF)  # Use station interface
sta.active(True)  # Activate the interface
sta.disconnect()  # Disconnect any existing connections (for ESP8266)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)  # Activate ESP-NOW
peer = b'\xb0\xa7\x32\x2b\xbd\xc4'  # MAC address of peer's Wi-Fi interface
e.add_peer(peer)  # Add peer to the ESP-NOW network

DEVICE_ID = 'SmartHome'  # Define the device ID

############################### OLED PART ##########################################

# Initialize I2C interface for OLED display
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128  # Define OLED width
oled_height = 64  # Define OLED height
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)  # Initialize OLED display
oled.invert(False)  # Set OLED display to normal mode

############################### MQ9 PART ##########################################

# Initialize MQ-9 sensor
analog_pin = 32  # Analog pin on ESP32
digital_pin = 25  # Digital pin on ESP32
mq9_sensor = MQ9(analog_pin, digital_pin)  # Create MQ-9 sensor object

############################### PIR PART ##########################################

# Initialize PIR sensor
pir_sensor_pin = 19  # GPIO pin connected to the PIR sensor
pir_sensor = PIRSensor(pir_sensor_pin)  # Create PIR sensor object

############################### FLAMESENSOR PART ##########################################

# Initialize flame sensor
flame_sensor = FlameSensor(analog_pin=33, digital_pin=5)  # Create flame sensor object

############################### TIMERS PART ##########################################

# Handler function to update OLED display with sensor readings
def timer1_handler(t):
    lectura = HTU21D.HTU21D(22, 21)  # Initialize HTU21D sensor
    hum = round(lectura.humidity)  # Read and round humidity value
    temp = round(lectura.temperature)  # Read and round temperature value

    temperature_string = str(temp)  # Convert temperature to string
    humidity_string = str(hum)  # Convert humidity to string

    # Read gas concentrations from MQ-9 sensor
    co_gas, smoke_gas, lpg_gas = mq9_sensor.read_gas_concentration()
    co_gas_round = round(co_gas)  # Round CO gas concentration
    co_gas_round_string = str(co_gas_round)  # Convert CO gas concentration to string

    # Display sensor readings on OLED
    oled.text("Temperature: ", 0, 20)
    oled.text(temperature_string, 100, 20)
    oled.text("Humidity: ", 0, 30)
    oled.text(humidity_string, 100, 30)
    oled.text("CO gas: ", 0, 40)
    oled.text(co_gas_round_string, 100, 40)
    oled.show()  # Update OLED display
    oled.fill(0)  # Clear OLED display

# Function to send sensor data via ESP-NOW
def send_data(t):
    lectura = HTU21D.HTU21D(22, 21)  # Initialize HTU21D sensor
    hum = lectura.humidity  # Read humidity value
    temp = lectura.temperature  # Read temperature value

    # Read gas concentrations from MQ-9 sensor
    co_gas, smoke_gas, lpg_gas = mq9_sensor.read_gas_concentration()
    motion_detected = pir_sensor.check_motion()  # Check for motion detection
    flame_detected = flame_sensor.read_sensor()  # Check for flame detection

    # Create data dictionary
    data = {
        'device_id': DEVICE_ID,
        'temperature': temp,
        'humidity': hum,
        'co_gas': co_gas,
        'smoke_gas': smoke_gas,
        'lpg_gas': lpg_gas
    }

    # Add motion detection info to data
    if motion_detected:
        data['motion_detected'] = True
    else:
        data['motion_detected'] = False

    # Add flame detection info to data
    if flame_detected == 1:
        data['flame_detected'] = True
    else:
        data['flame_detected'] = False

    print(data)  # Print data to console
    json_data = ujson.dumps(data)  # Convert data to JSON format
    e.send(peer, json_data)  # Send data to peer via ESP-NOW

# Initialize timers
timer1 = Timer(1)
timer3 = Timer(3)

# Configure timer1 to periodically update OLED display
timer1.init(period=2000, mode=Timer.PERIODIC, callback=timer1_handler)

# Configure timer3 to periodically send data via ESP-NOW
timer3.init(period=2000, mode=Timer.PERIODIC, callback=send_data)

