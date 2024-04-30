#from machine import Pin, ADC
#import time

#analogPin = ADC(Pin(4))
#digitalPin = Pin(35, Pin.IN)


#analogPinValue = analogPin.read()
#digitalPinValue = digitalPin.value()

#THRESHOLD = 1000 
                
#while True:
#    value = analogPin.read()  # Read the analog value from the sensor
#    moisture =  (100 - ((value/4095.00) * 100 ))
#    print(value)
#    time.sleep_ms(1000) 






#print(analogPinValue)
#print(digitalPinValue)




from machine import Pin, SoftI2C
from machine import Pin, ADC
import time

# Soil Moisture
soil = ADC(Pin(4))
m = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

# START
text = 'Starting...'

while True:
    try:
        soil.read()
        time.sleep(2)
        m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
        moisture = '{:.1f} %'.format(m)
        print('Soil Moisture:', moisture)
        lcd.clear()
        lcd.putstr('Soil Moisture: ')
        lcd.move_to(0,1)
        lcd.putstr(moisture)
        time.sleep(5)
    except:
        pass


