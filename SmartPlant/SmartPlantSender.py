import time
from machine import Pin, SoftI2C, ADC
import network
import espnow
import neopixel
from machine import RTC
import ntptime
from machine import Timer
from SoilMoisture import SoilMoistureSensor


# Initialize the soil moisture sensor
soil_sensor = SoilMoistureSensor(pin1=32, pin2=33)


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xb0\xa72+\xbd\xc4'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

# Identifiers
DEVICE_ID = 'SmartPlant'

############################### Relay Code ##########################################
relay_pin = 25  # Replace with the GPIO pin number connected to the relay module

# Initialize the GPIO pin as an output
relay = Pin(relay_pin, Pin.OUT)
relay.value(1)


def control_pump(on_time):
    relay.value(0) # Turn on the pump
    time.sleep(on_time)  # Wait for specified time (in seconds)
    relay.value(1)  # Turn off the pump


############################### NeoPixel Code ##########################################

n = 64
p = Pin(14, Pin.OUT)
np = neopixel.NeoPixel(p, n)

def police():
    np.fill((90,0,0))
    np.write()

def policeOFF():
    np.fill((0,0,0))
    np.write()

############################### RTC Code and Wifi ##########################################

wifi_ssid = "IoTnetwork"
wifi_password = "123456789IoT"

wlan = network.WLAN(network.STA_IF)  # Initialize the WLAN (Station mode)
wlan.active(True)                    # Activate the WLAN interface

if not wlan.isconnected():
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

TIMEZONE_OFFSET = 2

# Get UTC time from NTP server and set it to RTC
ntptime.host = "cz.pool.ntp.org"
ntptime.settime()

# Create an independent clock object
rtc = RTC()
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
# Update timezone
rtc.init((year, month, day, wday, hrs+TIMEZONE_OFFSET, mins, secs, subsecs))

DEVICE_ID = 'SmartPlant'

def send_data():
    moisture = soil_sensor.read_soil_moisture()
    data = {
        'device_id': DEVICE_ID,
        'soil_moisture': moisture
    }
    e.send(peer, str(data))

timer0 = Timer(0)
timer0.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: send_data())



