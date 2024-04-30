import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient
import HTU21D


lectura = HTU21D.HTU21D(22,21)


#Enter your wifi SSID and password below.
wifi_ssid = "IoTnetwork"
wifi_password = "123456789IoT"

#Enter your AWS IoT endpoint. 
aws_endpoint = b'a3d0i7yuvfp6ut-ats.iot.us-east-1.amazonaws.com'

#If you followed the blog, these names are already set.
thing_name = "ThingESP32"
client_id = "esp32"
private_key = "private.pem.key"
private_cert = "cert.pem.crt"
topic_pub = b"esp32/pub"
topic_sub= b"esp/sub"
#Read the files used to authenticate to AWS IoT Core
with open(private_key, 'r') as f:
    key = f.read()
with open(private_cert, 'r') as f:
    cert = f.read()

#These are the topics we will subscribe to. We will publish updates to /update.
#We will subscribe to the /update/delta topic to look for changes in the device shadow.
#topic_pub = "$aws/things/" + thing_name + "/shadow/update"
#topic_sub = "$aws/things/" + thing_name + "/shadow/update/delta"
ssl_params = {"key":key, "cert":cert, "server_side":False}
info = os.uname()

#Connect to the wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message)


#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
try:
    mqtt = mqtt_connect()
    #mqtt.set_callback(mqtt_subscribe)
    #mqtt.subscribe(topic_sub)
except:
    print("Unable to connect to MQTT.")


while True:
#Check for messages.
    try:
        mqtt.check_msg()
    except:
        print("Unable to check for messages.")

    hum = lectura.humidity
    temp = lectura.temperature
    DateTime = lectura.dateTime
    mesg = ujson.dumps({
        "state":{
            "reported": {
#                "device": {
#                    "client": client_id,
#                   "hardware": info[0],
#                   "firmware": info[2]
#               },
                "SensorData":{
                    "ActualHumidity" : hum,
                    "ActualTemperature" : temp,
                    "CurrentDateTime ":  DateTime
                    }
            }
        }
    })

#Using the message above, the device shadow is updated.
    try:
        mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Unable to publish message.")
    time.sleep(60)