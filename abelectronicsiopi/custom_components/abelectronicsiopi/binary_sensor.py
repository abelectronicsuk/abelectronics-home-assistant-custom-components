"""Support for binary sensor using I2C abelectronicsiopi chip."""
from custom_components.abelectronicsiopi.IOPi import IOPi
import voluptuous as vol
import logging
from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.const import DEVICE_DEFAULT_NAME
import homeassistant.helpers.config_validation as cv

CONF_INVERT_LOGIC = "invert_logic"
CONF_I2C_ADDRESS = "i2c_address"
CONF_PINS = "pins"
CONF_PULL_MODE = "pull_mode"

DEFAULT_INVERT_LOGIC = False
DEFAULT_I2C_ADDRESS = 0x20
DEFAULT_PULL_MODE = True

_SENSORS_SCHEMA = vol.Schema({cv.positive_int: cv.string})

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PINS): _SENSORS_SCHEMA,
        vol.Optional(CONF_INVERT_LOGIC, default=DEFAULT_INVERT_LOGIC): cv.boolean,
        vol.Optional(CONF_PULL_MODE, default=DEFAULT_PULL_MODE): cv.boolean,
        vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
    }
)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the abelectronicsiopi binary sensors."""
    pull_mode = config[CONF_PULL_MODE]
    invert_logic = config[CONF_INVERT_LOGIC]

    iopi = IOPi(config.get(CONF_I2C_ADDRESS), False)

    binary_sensors = []
    pins = config[CONF_PINS]

    for pin_num, pin_name in pins.items():
        binary_sensors.append(abelectronicsiopiBinarySensor(pin_name, pin_num, pull_mode, invert_logic, iopi))
    add_devices(binary_sensors, True)


class abelectronicsiopiBinarySensor(BinarySensorEntity):
    """Represent a binary sensor that uses abelectronicsiopi."""

    io_bus = None
    target_pin = None
    _state = False

    def __init__(self, pin_name, pin, pull_mode, invert_logic, bus):
        """Initialize the pin."""
        try:
            self._state = None
            self._name = pin_name
            self.target_pin = pin
            self.io_bus = bus

            if pull_mode:
                self.io_bus.set_pin_pullup(self.target_pin, 1)
            else:
                self.io_bus.set_pin_pullup(self.target_pin, 0)

            self.io_bus.set_pin_direction(self.target_pin, 1)

            if invert_logic:
                self.io_bus.invert_pin(self.target_pin, 1)
            else:
                self.io_bus.invert_pin(self.target_pin, 0)
        except Exception as e:
            _LOGGER.error(e)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the entity."""
        try:
            self._state = self.io_bus.read_pin(self.target_pin)
        except Exception as e:
            _LOGGER.error(e)
        return self._state

    def update(self):
        """Update the GPIO state."""
        try:
            self._state = self.io_bus.read_pin(self.target_pin)
        except Exception as e:
            _LOGGER.error(e)
