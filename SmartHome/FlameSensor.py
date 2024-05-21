from machine import Pin, ADC
import time

class FlameSensor:
    def __init__(self, analog_pin_num, digital_pin_num):
        self.analog_pin = ADC(Pin(analog_pin_num))
        self.digital_pin = Pin(digital_pin_num, Pin.IN)
        self.digital_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.interrupt_handler)
        
    def interrupt_handler(self, pin):
        # Print flame detected message
        print("Fire detected!")
        
    def read_sensor(self):
        # Read analog value from sensor
        sensor_value = self.analog_pin.read()
        return sensor_value

    def map_analog_value(self, value, in_min=0, in_max=4095, out_min=0, out_max=3):
        """
        Function to map the analog value to a specified range.
        """
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def check_flame(self):
        sensor_value = self.read_sensor()
        mapped_value = self.map_analog_value(sensor_value)
        
        if mapped_value == 0:
            print("Fire detected within 20 cm!")
        elif mapped_value == 1:
            print("Fire detected at distances from 20 to 80 cm!")
        else:
            print("No fire detected.")
    
# Initialize the flame sensor with the appropriate pins
flame_sensor = FlameSensor(analog_pin_num=33, digital_pin_num=5)

