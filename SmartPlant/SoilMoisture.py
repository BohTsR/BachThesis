from machine import Pin, ADC

class SoilMoistureSensor:
    def __init__(self, pin1, pin2, min_moisture=0, max_moisture=4095):
        self.soil1 = ADC(Pin(pin1))
        self.soil2 = ADC(Pin(pin2))

        self.min_moisture = min_moisture
        self.max_moisture = max_moisture

        # Initialize ADC settings
        self.soil1.atten(ADC.ATTN_11DB)  # Full range: 3.3v
        self.soil1.width(ADC.WIDTH_12BIT)  # range 0 to 4095

        self.soil2.atten(ADC.ATTN_11DB)  # Full range: 3.3v
        self.soil2.width(ADC.WIDTH_12BIT)  # range 0 to 4095

    def read_soil_moisture(self):
        # Read analog value from soil moisture sensor
        m1 = (self.max_moisture - self.soil1.read()) * 100 / (self.max_moisture - self.min_moisture)
        m2 = (self.max_moisture - self.soil2.read()) * 100 / (self.max_moisture - self.min_moisture)
        
        # Calculate moisture percentage (adjust as per sensor calibration)
        mois = (m1 + m2) / 2
        return mois
