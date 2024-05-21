from machine import Pin, ADC

class MQ9:
    def __init__(self, analog_pin, digital_pin, r0=1.62, vcc=5.0):
        """
        Initialize the MQ-9 sensor.
        
        :param analog_pin: ADC pin for reading analog values.
        :param digital_pin: Digital pin for detecting gas presence.
        :param r0: Sensor resistance in clean air (default: 1.62).
        :param vcc: Supply voltage (default: 5.0).
        """
        self.adc = ADC(Pin(analog_pin))
        self.digital_pin = Pin(digital_pin, Pin.IN)
        self.r0 = r0
        self.vcc = vcc

    def read_gas_concentration(self):
        """
        Function to read the gas concentration values from the MQ-9 sensor.
        
        :return: A tuple with CO gas, smoke gas, and LPG gas concentrations in ppm.
        """
        sensor_value = self.adc.read()
        sensor_volt = sensor_value / 4095.0 * self.vcc
        rs_gas = (self.vcc - sensor_volt) / sensor_volt
        ratio = rs_gas / self.r0

        co_gas = self.calculate_co_ppm(ratio)
        smoke_gas = self.calculate_smoke_ppm(ratio)
        lpg_gas = self.calculate_lpg_ppm(ratio)

        return co_gas, smoke_gas, lpg_gas

    def calculate_co_ppm(self, ratio):
        """
        Function to calculate CO ppm from the resistance ratio.
        """
        if ratio <= 1.0:
            return 100 * ratio  # Simplified conversion, need real calibration curve
        else:
            return 100 * (ratio ** (-1.25))

    def calculate_smoke_ppm(self, ratio):
        """
        Function to calculate smoke ppm from the resistance ratio.
        """
        return 50 * (ratio ** (-1.5))

    def calculate_lpg_ppm(self, ratio):
        """
        Function to calculate LPG ppm from the resistance ratio.
        """
        return 200 * (ratio ** (-1.3))

    def is_gas_detected(self):
        """
        Function to check if gas is detected based on the digital pin.
        
        :return: True if gas is detected, False otherwise.
        """
        return self.digital_pin.value() == 0  # Assuming 0 indicates gas detected, adjust if needed
