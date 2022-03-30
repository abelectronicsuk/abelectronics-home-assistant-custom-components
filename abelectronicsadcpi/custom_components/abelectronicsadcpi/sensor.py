"""Sensor platform for abelectronicsadcpi."""
from custom_components.abelectronicsadcpi.ADCPi import ADCPi
import voluptuous as vol
import asyncio
import concurrent.futures
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import DEVICE_DEFAULT_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
from homeassistant.util import Throttle
from homeassistant.helpers.entity import ToggleEntity

CONF_BITRATE = "bitrate"
CONF_PGA= "pga"
CONF_I2C_ADDRESS1 = "i2c_address"
CONF_I2C_ADDRESS2 = "i2c_address2"

DEFAULT_NAME = 'ADC Pi Sensor'
DEFAULT_BITRATE = 16
DEFAULT_PGA = 1
DEFAULT_I2C_ADDRESS1 = 0x68
DEFAULT_I2C_ADDRESS2 = 0x69

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=0.5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_BITRATE, default=DEFAULT_BITRATE): vol.Coerce(int),
        vol.Optional(CONF_PGA, default=DEFAULT_PGA): vol.Coerce(int),
        vol.Optional(CONF_I2C_ADDRESS1, default=DEFAULT_I2C_ADDRESS1): vol.Coerce(int),
        vol.Optional(CONF_I2C_ADDRESS2, default=DEFAULT_I2C_ADDRESS2): vol.Coerce(int),
    }
)

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Setup the sensor platform."""
    i2caddress = config.get(CONF_I2C_ADDRESS1)
    i2caddress2 = config.get(CONF_I2C_ADDRESS2)
    bitrate = config.get(CONF_BITRATE)
    adc = ADCPi(i2caddress, i2caddress2, bitrate)
    adc.pga = config.get(CONF_PGA)
    async_add_devices([abelectronicsadcpiSensor(adc)])


class abelectronicsadcpiSensor(Entity):

    """
    Control the MCP3424 ADC on the ADC Pi.
    """
    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0
    v5 = 0
    v6 = 0
    v7 = 0
    v8 = 0
    
    def getVals(self):
        self.v1 = self._adc.read_voltage(1)
        self.v2 = self._adc.read_voltage(2)
        self.v3 = self._adc.read_voltage(3)
        self.v4 = self._adc.read_voltage(4)
        self.v5 = self._adc.read_voltage(5)
        self.v6 = self._adc.read_voltage(6)
        self.v7 = self._adc.read_voltage(7)
        self.v8 = self._adc.read_voltage(8)

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
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr['input1'] = self.v1
        attr['input2'] = self.v2
        attr['input3'] = self.v3
        attr['input4'] = self.v4
        attr['input5'] = self.v5
        attr['input6'] = self.v6
        attr['input7'] = self.v7
        attr['input8'] = self.v8
        return attr

    @asyncio.coroutine
    def async_update(self):
        """Fetch new state data."""        
        self.getVals()
        self._state = self._state