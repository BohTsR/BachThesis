from machine import SoftI2C, Pin
import time
import utime

class HTU21D(object):
    ADDRESS = 0x40
    ISSUE_TEMP_ADDRESS = 0xE3
    ISSUE_HU_ADDRESS = 0xE5

    def __init__(self, scl, sda):
        
        scl(int): 22
        sda(int): 21
        self.i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda), freq=100000)


    def _crc_check(self, value):
        
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def _issue_measurement(self, write_address):
        """Issue a measurement.
        Args:
            write_address (int): address to write to
        :return:
        """
        self.i2c.start()
        self.i2c.writeto_mem(int(self.ADDRESS), int(write_address), '')
        self.i2c.stop()
        time.sleep_ms(50)
        data = bytearray(3)
        self.i2c.readfrom_into(self.ADDRESS, data)
        if not self._crc_check(data):
            raise ValueError()
        raw = (data[0] << 8) + data[1]
        raw &= 0xFFFC
        return raw

    @property
    def temperature(self):
        """Calculate temperature"""
        raw = self._issue_measurement(self.ISSUE_TEMP_ADDRESS)
        return -46.85 + (175.72 * raw / 65536)

    @property
    def humidity(self):
        """Calculate humidity"""
        raw =  self._issue_measurement(self.ISSUE_HU_ADDRESS)
        return -6 + (125.0 * raw / 65536)

    @property
    def dateTime(current_time):
        # Get the current time in seconds since the Unix epoch
        current_time = utime.time()
        # Convert the current time to a tuple representing the date and time
        # The tuple format is: (year, month, day, hour, minute, second, weekday, day_of_year)
        time_tuple = utime.localtime(current_time)
        # Print the current date and time
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # Format the date and time
        formatted_time = "{0} {1:02d} {2} {3:02d}:{4:02d}".format(
        days[time_tuple[6]],  # Day of the week (0 to 6, where 0 is Monday)
        time_tuple[2],  # Day of the month
        months[time_tuple[1] - 1],  # Month (1 to 12)
        time_tuple[3],  # Hour
        time_tuple[4]   # Minute
        )
        print("Current Date and Time:\n ", formatted_time)
