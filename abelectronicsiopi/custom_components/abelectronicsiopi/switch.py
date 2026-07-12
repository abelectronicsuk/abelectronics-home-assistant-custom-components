"""Support for switch sensor using I2C abelectronicsiopi chip."""
from custom_components.abelectronicsiopi.IOPi import IOPi
import voluptuous as vol
import logging
import threading
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import DEVICE_DEFAULT_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import ToggleEntity



CONF_INVERT_LOGIC = "invert_logic"
CONF_I2C_ADDRESS = "i2c_address"
CONF_PINS = "pins"

DEFAULT_INVERT_LOGIC = False
DEFAULT_I2C_ADDRESS = 0x20

_SWITCHES_SCHEMA = vol.Schema({cv.positive_int: cv.string})

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PINS): _SWITCHES_SCHEMA,
        vol.Optional(CONF_INVERT_LOGIC, default=DEFAULT_INVERT_LOGIC): cv.boolean,
        vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the abelectronicsiopi devices."""
    try:
        invert_logic = config.get(CONF_INVERT_LOGIC)
        io_bus = IOPi(config.get(CONF_I2C_ADDRESS), False)
        bus_lock = threading.Lock()
        switches = []
        pins = config.get(CONF_PINS)
        for pin_num, pin_name in pins.items():
            switches.append(abelectronicsiopiSwitch(pin_name, pin_num, invert_logic, io_bus, bus_lock))
        add_entities(switches)
    except Exception as e:
        _LOGGER.error(e)

class abelectronicsiopiSwitch(ToggleEntity):
    """Representation of an abelectronicsiopi output pin."""

    io_bus = None
    target_pin = None
    _state = False

    def __init__(self, pinname, pin, invert_logic, bus, bus_lock):
        """Initialise the pin."""
        try:
            self._name = pinname
            self.target_pin = pin
            self.io_bus = bus
            self._bus_lock = bus_lock
            pin_direction = self.io_bus.get_pin_direction(self.target_pin)
            if pin_direction == 1:
                self.io_bus.set_pin_direction(self.target_pin, 0)
            self._state = self.io_bus.read_pin(self.target_pin)
            if invert_logic:
                self.io_bus.invert_pin(self.target_pin, 1)
        except Exception as e:
            _LOGGER.error(e)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def is_on(self):
        """Return true if the device is on."""
        return self._state

    @property
    def assumed_state(self):
        """Return true if optimistic updates are used."""
        return True

    def turn_on(self, **kwargs):
        """Turn the device on."""
        try:
            with self._bus_lock:
                self.io_bus.write_pin(self.target_pin, 1)
            self._state = True
            self.schedule_update_ha_state()
        except Exception as e:
            _LOGGER.error(e)

    def turn_off(self, **kwargs):
        """Turn the device off."""
        try:
            with self._bus_lock:
                self.io_bus.write_pin(self.target_pin, 0)
            self._state = False
            self.schedule_update_ha_state()
        except Exception as e:
            _LOGGER.error(e)
