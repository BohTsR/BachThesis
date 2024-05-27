import network
import espnow
import time
import ujson
import urequests  # Use urequests to send HTTP requests
from machine import RTC, Timer
import ntptime

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
#sta.disconnect()  # Disconnect from any previous network connections

e = espnow.ESPNow()
e.active(True)

# MAC addresses of the slave ESP32 devices
SMART_HOME_MAC  = b'\xe4e\xb8 \xa4 '   # Replace with actual MAC address of SmartHome device
SMART_PLANT_MAC = b'\xb0\xa72\xdb7t'  # Replace with actual MAC address of SmartPlant device
e.add_peer(SMART_HOME_MAC)
e.add_peer(SMART_PLANT_MAC)

############################### AWS CODE ##########################################
wifi_ssid = "IoTnetwork"
wifi_password = "123456789IoT"

# AWS Lambda function URL obtained from API Gateway deployment
lambda_url = 'https://m8luslbtbc.execute-api.us-east-1.amazonaws.com/prod/UploadDataToS3'  # Replace with your actual API Gateway URL

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

############################### RTC CODE ##########################################

TIMEZONE_OFFSET = 2

# Get UTC time from NTP server and set it to RTC
ntptime.host = "cz.pool.ntp.org"
ntptime.settime()
print("Local RTC synchronized")

# Create an independent clock object
rtc = RTC()

# Print UTC time after NTP update
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
# Update timezone
rtc.init((year, month, day, wday, hrs, mins, secs, subsecs))

############################### Main Runner ##########################################

def receive_data_from_smart_home(t):
    host, msg = e.recv()
    if host == SMART_HOME_MAC and msg:
        process_received_data(msg, "SmartHome")

def receive_data_from_smart_plant():
    host, msg = e.recv()
    if host == SMART_PLANT_MAC and msg:
        process_received_data(msg, "SmartPlant")

def process_received_data(msg, device_id):
    try:
        data_str = msg.decode('utf-8')
        data = ujson.loads(data_str)
        print(f"Data received from {device_id}:", data)
        
        (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
        rtc.init((year, month, day, wday, hrs, mins, secs, subsecs))
        
        # Convert current time to a Unix timestamp
        current_time = time.mktime((year, month, day, hrs, mins, secs, wday, 0))
        
        # Convert received data to JSON string
        data['timestamp'] = int(current_time+946684800)  # Unix timestamp for key value
        data['Readable_Time'] = "{:02d}:{:02d}-{:02d}.{:02d}.{:04d}".format(hrs, mins, day, month, year)  # Human-readable format
        data['device_id'] = device_id
        
        message = ujson.dumps(data)
        
        # Send data to AWS Lambda function
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(lambda_url, data=message, headers=headers)
        print("Lambda Response:", response.text)
    except ValueError as e:
        print("Failed to decode JSON:", e)
        print("Received message:", msg)
    except Exception as e:
        print("An error occurred:", e)

# Timers to receive data periodically and send to AWS Lambda
timer_smart_home = Timer(0)
timer_smart_home.init(period=2000, mode=Timer.PERIODIC, callback=receive_data_from_smart_home)

timer_smart_plant = Timer(1)
timer_smart_plant.init(period=10000, mode=Timer.PERIODIC, callback=lambda t: receive_data_from_smart_plant())
