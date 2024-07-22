"""Support for switch sensor using I2C abelectronicsiopi chip."""
from custom_components.abelectronicsiopi.IOPi import IOPi
import voluptuous as vol

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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PINS): _SWITCHES_SCHEMA,
        vol.Optional(CONF_INVERT_LOGIC, default=DEFAULT_INVERT_LOGIC): cv.boolean,
        vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the abelectronicsiopi devices."""
    invert_logic = config.get(CONF_INVERT_LOGIC)
    iopi = IOPi(config.get(CONF_I2C_ADDRESS), False)
    switches = []
    pins = config.get(CONF_PINS)
    for pin_num, pin_name in pins.items():
        switches.append(abelectronicsiopiSwitch(pin_name, pin_num, invert_logic, iopi))
    add_entities(switches)

class abelectronicsiopiSwitch(ToggleEntity):
    """Representation of a  abelectronicsiopi output pin."""

    iobus = None
    targetpin = None
    _state = False

    def __init__(self, pinname, pin, invert_logic, bus):
        """Initialize the pin."""
        self._name = pinname
        self.targetpin = pin
        self.iobus = bus
        self.iobus.set_pin_direction(self.targetpin, 0)
        self.iobus.write_pin(self.targetpin, 0)
        if invert_logic == True:
            self.iobus.invert_pin(self.targetpin, 1)

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
        """Return true if device is on."""
        return self._state

    @property
    def assumed_state(self):
        """Return true if optimistic updates are used."""
        return True

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self.iobus.write_pin(self.targetpin, 1)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self.iobus.write_pin(self.targetpin, 0)
        self._state = False
        self.schedule_update_ha_state()