"""
Support for ADC Pi 8 channel ADC from www.ablectronics.co.uk.

For more details about this board, please refer to the documentation at
https://www.ablectronics.co.uk
"""
import asyncio
from datetime import timedelta
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA

import re
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)
CONF_I2C_BUS = 'i2c_bus'
CONF_I2C_ADDRESS1 = 'i2c_address'
CONF_I2C_ADDRESS2 = 'i2c_address2'
CONF_BITRATE = 'bitrate'
CONF_PGA = 'pga'

DEFAULT_I2C_BUS = 1
DEFAULT_NAME = 'ADC Pi Sensor'
DEFAULT_I2C_ADDRESS1 = '0x68'
DEFAULT_I2C_ADDRESS2 = '0x69'
DEFAULT_BITRATE = 18
DEFAULT_PGA = 1

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=0.5)

REQUIREMENTS = ['i2csense==0.0.3',
                'smbus-cffi==0.5.1']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): vol.Coerce(int),
    vol.Optional(CONF_I2C_ADDRESS1, default=DEFAULT_I2C_ADDRESS1): vol.Coerce(int),
    vol.Optional(CONF_I2C_ADDRESS2, default=DEFAULT_I2C_ADDRESS2): vol.Coerce(int),
    vol.Optional(CONF_BITRATE, default=DEFAULT_BITRATE): vol.Coerce(int),
    vol.Optional(CONF_PGA, default=DEFAULT_PGA): vol.Coerce(int),
    
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Setup the sensor platform."""
    import smbus
    i2caddress = config.get(CONF_I2C_ADDRESS1)
    i2caddress2 = config.get(CONF_I2C_ADDRESS2)
    pga = config.get(CONF_PGA)
    bitrate = config.get(CONF_BITRATE)
    bus = smbus.SMBus(1)
    adc = ADCPi(i2caddress, i2caddress2, pga, bitrate, bus)
    async_add_devices([ADCPiSensor(adc)])


class ADCPiSensor(Entity):

    """
    Control the MCP3424 ADC on the ADC Pi Plus and ADC Pi Zero
    """
    
    """Representation of an ADC Pi from abelectronics.co.uk."""
    def __init__(self, adc):
        """Initialize the sensor."""
        self._state = None
        self._adc = adc
        self._data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self, first_reading=False):
      self.sensor.update(first_reading)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'ADCPi'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'V'

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr['input1'] = self._adc.read_voltage(1)
        attr['input2'] = self._adc.read_voltage(2)
        attr['input3'] = self._adc.read_voltage(3)
        attr['input4'] = self._adc.read_voltage(4)
        attr['input5'] = self._adc.read_voltage(5)
        attr['input6'] = self._adc.read_voltage(6)
        attr['input7'] = self._adc.read_voltage(7)
        attr['input8'] = self._adc.read_voltage(8)
        return attr
        
    @asyncio.coroutine
    def async_update(self):
        """Fetch new state data."""
        self._state = self._state
        


class ADCPi:
    """
    Control the MCP3424 ADC on the ADC Pi Plus and ADC Pi Zero
    """
    # internal variables
    __adc1_address = 0x68
    __adc2_address = 0x69

    __adc1_conf = 0x9C
    __adc2_conf = 0x9C

    __adc1_channel = 0x01
    __adc2_channel = 0x01

    __bitrate = 18  # current bitrate
    __conversionmode = 1  # Conversion Mode
    __pga = float(0.5)  # current pga setting
    __lsb = float(0.0000078125)  # default lsb value for 18 bit
    __signbit = 0  # stores the sign bit for the sampled value

    # create byte array and fill with initial values to define size
    __adcreading = bytearray([0, 0, 0, 0])

    __bus = None

    # local methods

    

    def __setchannel(self, channel):
        # internal method for updating the config to the selected channel
        if channel < 5:
            if channel != self.__adc1_channel:
                self.__adc1_channel = channel
                if channel == 1:  # bit 5 = 0, bit 6 = 0
                    self.__adc1_conf = self.__adc1_conf & ~(1 << 5) & ~(1 << 6)
                elif channel == 2:  # bit 5 = 1, bit 6 = 0
                    self.__adc1_conf = self.__adc1_conf | (1 << 5) & ~(1 << 6)
                elif channel == 3:  # bit 5 = 0, bit 6 = 1
                    self.__adc1_conf = self.__adc1_conf & ~(1 << 5) | (1 << 6)
                elif channel == 4:  # bit 5 = 1, bit 6 = 1
                    self.__adc1_conf = self.__adc1_conf | (1 << 5) | (1 << 6)
        else:
            if channel != self.__adc2_channel:
                self.__adc2_channel = channel
                if channel == 5:  # bit 5 = 0, bit 6 = 0
                    self.__adc2_conf = self.__adc2_conf & ~(1 << 5) & ~(1 << 6)
                elif channel == 6:  # bit 5 = 1, bit 6 = 0
                    self.__adc2_conf = self.__adc2_conf | (1 << 5) & ~(1 << 6)
                elif channel == 7:  # bit 5 = 0, bit 6 = 1
                    self.__adc2_conf = self.__adc2_conf & ~(1 << 5) | (1 << 6)
                elif channel == 8:  # bit 5 = 1, bit 6 = 1
                    self.__adc2_conf = self.__adc2_conf | (1 << 5) | (1 << 6)
        return

    # init object with i2caddress, default is 0x68, 0x69 for ADCoPi board
    def __init__(self, address=0x68, address2=0x69, pga=1, rate=18, bus=None):

        self.__bus = bus
        self.__adc1_address = address
        self.__adc2_address = address2
        #self.set_pga(pga)
        self.set_bit_rate(rate)

    def read_voltage(self, channel):
        """
        returns the voltage from the selected adc channel - channels 1 to 8
        """
        raw = self.read_raw(channel)
        voltage = float(0.0)
        if not self.__signbit:
            voltage = float(
                (raw * (self.__lsb / self.__pga)) * 2.471)

        return voltage

    def read_raw(self, channel):
        """
        reads the raw value from the selected adc channel - channels 1 to 8
        """
        high = 0
        low = 0
        mid = 0
        cmdbyte = 0

        # get the config and i2c address for the selected channel
        self.__setchannel(channel)
        if channel < 5:
            config = self.__adc1_conf
            address = self.__adc1_address
        elif channel < 9:
            config = self.__adc2_conf
            address = self.__adc2_address
        else:
            raise ValueError('read_raw: channel out of range')

        # if the conversion mode is set to one-shot update the ready bit to 1
        if self.__conversionmode == 0:
            config = config | (1 << 7)
            self.__bus.write_byte(address, config)
            config = config & ~(1 << 7)  # reset the ready bit to 0
        # keep reading the adc data until the conversion result is ready
        while True:
            __adcreading = self.__bus.read_i2c_block_data(address, config, 4)
            if self.__bitrate == 18:
                high = __adcreading[0]
                mid = __adcreading[1]
                low = __adcreading[2]
                cmdbyte = __adcreading[3]
            else:
                high = __adcreading[0]
                mid = __adcreading[1]
                cmdbyte = __adcreading[2]
            # check if bit 7 of the command byte is 0.
            if(cmdbyte & (1 << 7)) == 0:
                break

        self.__signbit = False
        raw = 0
        # extract the returned bytes and combine in the correct order
        if self.__bitrate == 18:
            raw = ((high & 0x03) << 16) | (mid << 8) | low
            self.__signbit = bool(raw & (1 << 17))
            raw = raw & ~(1 << 17)  # reset sign bit to 0

        elif self.__bitrate == 16:
            raw = (high << 8) | mid
            self.__signbit = bool(raw & (1 << 15))
            raw = raw & ~(1 << 15)  # reset sign bit to 0

        elif self.__bitrate == 14:
            raw = ((high & 0b00111111) << 8) | mid
            self.__signbit = bool(raw & (1 << 13))
            raw = raw & ~(1 << 13)  # reset sign bit to 0

        elif self.__bitrate == 12:
            raw = ((high & 0x0f) << 8) | mid
            self.__signbit = bool(raw & (1 << 11))
            raw = raw & ~(1 << 11)  # reset sign bit to 0

        return raw

    def set_pga(self, gain):
        """
        PGA gain selection
        1 = 1x
        2 = 2x
        4 = 4x
        8 = 8x
        """

        if gain == 1:
            # bit 0 = 0, bit 1 = 0
            self.__adc1_conf = self.__adc1_conf & ~(1 << 0) & ~(1 << 1)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 0) & ~(1 << 1)
            self.__pga = 0.5
        elif gain == 2:
            # bit 0 = 1, bit 1 = 0
            self.__adc1_conf = self.__adc1_conf & ~(1 << 1) | (1 << 0)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 1) | (1 << 0)
            self.__pga = 1.0
        elif gain == 4:
            # bit 0 = 0, bit 1 = 1
            self.__adc1_conf = self.__adc1_conf & ~(1 << 0) | (1 << 1)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 0) | (1 << 1)
            self.__pga = 2.0
        elif gain == 8:
            # bit 0 = 1, bit 1 = 1
            self.__adc1_conf = self.__adc1_conf | (1 << 0) | (1 << 1)
            self.__adc2_conf = self.__adc2_conf | (1 << 0) | (1 << 1)
            self.__pga = 4.0
        else:
            raise ValueError('set_pga: gain out of range')

        self.__bus.write_byte(self.__adc1_address, self.__adc1_conf)
        self.__bus.write_byte(self.__adc2_address, self.__adc2_conf)
        return

    def set_bit_rate(self, rate):
        """
        sample rate and resolution
        12 = 12 bit (240SPS max)
        14 = 14 bit (60SPS max)
        16 = 16 bit (15SPS max)
        18 = 18 bit (3.75SPS max)
        """

        if rate == 12:
            # bit 2 = 0, bit 3 = 0
            self.__adc1_conf = self.__adc1_conf & ~(1 << 2) & ~(1 << 3)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 2) & ~(1 << 3)
            self.__bitrate = 12
            self.__lsb = 0.0005
        elif rate == 14:
            # bit 2 = 1, bit 3 = 0
            self.__adc1_conf = self.__adc1_conf & ~(1 << 3) | (1 << 2)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 3) | (1 << 2)
            self.__bitrate = 14
            self.__lsb = 0.000125
        elif rate == 16:
            # bit 2 = 0, bit 3 = 1
            self.__adc1_conf = self.__adc1_conf & ~(1 << 2) | (1 << 3)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 2) | (1 << 3)
            self.__bitrate = 16
            self.__lsb = 0.00003125
        elif rate == 18:
            # bit 2 = 1, bit 3 = 1
            self.__adc1_conf = self.__adc1_conf | (1 << 2) | (1 << 3)
            self.__adc2_conf = self.__adc2_conf | (1 << 2) | (1 << 3)
            self.__bitrate = 18
            self.__lsb = 0.0000078125
        else:
            raise ValueError('set_bit_rate: rate out of range')

        self.__bus.write_byte(self.__adc1_address, self.__adc1_conf)
        self.__bus.write_byte(self.__adc2_address, self.__adc2_conf)
        return

    def set_conversion_mode(self, mode):
        """
        conversion mode for adc
        0 = One shot conversion mode
        1 = Continuous conversion mode
        """
        if mode == 0:
            # bit 4 = 0
            self.__adc1_conf = self.__adc1_conf & ~(1 << 4)
            self.__adc2_conf = self.__adc2_conf & ~(1 << 4)
            self.__conversionmode = 0
        elif mode == 1:
            # bit 4 = 1
            self.__adc1_conf = self.__adc1_conf | (1 << 4)
            self.__adc2_conf = self.__adc2_conf | (1 << 4)
            self.__conversionmode = 1
        else:
            raise ValueError('set_conversion_mode: mode out of range')

        return
