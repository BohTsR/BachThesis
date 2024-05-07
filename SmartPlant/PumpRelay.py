import time
from machine import Pin, SoftI2C, ADC

# Define the GPIO pin connected to the relay module
relay_pin = 25  # Replace with the GPIO pin number connected to the relay module

# Initialize the GPIO pin as an output
relay = Pin(relay_pin, Pin.OUT)
relay.value(1)


# Soil Moisture
soil = ADC(Pin(32))
m = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

def read_soil_moisture():
    # Read analog value from soil moisture sensor
    soil.read()
    # Calculate moisture percentage (adjust as per sensor calibration)
    m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
    moisture_percentage = '{:.1f} %'.format(m)
    return moisture_percentage


def control_pump(on_time):
    relay.value(0) # Turn on the pump
    time.sleep(on_time)  # Wait for specified time (in seconds)
    relay.value(1)  # Turn off the pump


while True:
    # Read soil moisture
    moisture = read_soil_moisture()
    print("Soil Moisture:", moisture, "%")
    
    # Check if soil moisture is below threshold (e.g., 30%)
    if moisture < "63пш.0 %":
        print("Soil moisture is below threshold. Turning on pump...")
        control_pump(5)  # Turn on pump for 30 seconds
    
    # Wait for 3 minutes before repeating the cycle
    time.sleep(5)  # 3 minutes (180 seconds)



