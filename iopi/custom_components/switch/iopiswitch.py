"""
Support for IO Pi Port Expander from www.ablectronics.co.uk.

For more details about this board, please refer to the documentation at
https://www.ablectronics.co.uk
"""
import logging
import asyncio
import voluptuous as vol

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['i2csense==0.0.3',
                'smbus-cffi==0.5.1']

_LOGGER = logging.getLogger(__name__)

CONF_PINS = 'pins'
CONF_TYPE = 'digital'
CONF_INITIAL = 'initial'
CONF_I2C_BUS = 'i2c_bus'
CONF_I2C_AD = 'i2c_address'
CONF_INVERT_LOGIC = 'invert_logic'

DEFAULT_I2C_BUS = 1
DEFAULT_NAME = 'IOPi Switch'
DEFAULT_I2C_AD = '0x21'
DEFAULT_INVERT_LOGIC = False

PIN_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_INITIAL, default=False): cv.boolean,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PINS, default={}):
        vol.Schema({cv.positive_int: PIN_SCHEMA}),
    vol.Optional(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): vol.Coerce(int),
    vol.Optional(CONF_I2C_AD, default=DEFAULT_I2C_AD): vol.Coerce(int),
    vol.Optional(CONF_INVERT_LOGIC, default=DEFAULT_INVERT_LOGIC): cv.boolean,
})


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Arduino platform."""
    # Verify that Arduino board is present
    import smbus
    i2caddress = config.get(CONF_I2C_AD)
    invert_logic = config.get(CONF_INVERT_LOGIC)
    bus = smbus.SMBus(1)
    iopi = IOPi(i2caddress, bus)

    pins = config.get(CONF_PINS)

    switches = []
    for pinnum, pin in pins.items():
        switches.append(IOPISwitch(pinnum, pin, bus, iopi, invert_logic))
    async_add_devices(switches)


class IOPISwitch(SwitchDevice):
    """Representation of an IOPi switch."""

    def __init__(self, pin, options, bus, iopi, invert_logic):
        """Initialize the Pin."""
        self._pin = pin
        self._name = options.get(CONF_NAME)
        self.pin_type = CONF_TYPE
        self.direction = 'out'
        self._iopi = iopi
        self._invert_logic = invert_logic
        self._state = options.get(CONF_INITIAL)
        if self._state:
            self._iopi.write_pin(self._pin, 0 if self._invert_logic else 1)
        else:
            self._iopi.write_pin(self._pin, 1 if self._invert_logic else 0)

    @property
    def name(self):
        """Get the name of the pin."""
        return self._name

    @property
    def is_on(self):
        """Return true if pin is high/on."""
        return self._state

    def turn_on(self):
        """Turn the pin to high/on."""
        self._state = True
        self._iopi.write_pin(self._pin, 0 if self._invert_logic else 1)

    def turn_off(self):
        """Turn the pin to low/off."""
        self._state = False
        self._iopi.write_pin(self._pin, 1 if self._invert_logic else 0)


class IOPi(object):
    """
    The MCP23017 chip is split into two 8-bit ports.  port 0 controls pins
    1 to 8 while port 1 controls pins 9 to 16.
    When writing to or reading from a port the least significant bit
    represents the lowest numbered pin on the selected port.
    #
    """

    # Define registers values from datasheet
    IODIRA = 0x00  # IO direction A - 1= input 0 = output
    IODIRB = 0x01  # IO direction B - 1= input 0 = output
    # Input polarity A - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLA = 0x02
    # Input polarity B - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLB = 0x03
    # The GPINTEN register controls the interrupt-onchange feature for each
    # pin on port A.
    GPINTENA = 0x04
    # The GPINTEN register controls the interrupt-onchange feature for each
    # pin on port B.
    GPINTENB = 0x05
    # Default value for port A - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite from the register bit, an interrupt occurs.
    DEFVALA = 0x06
    # Default value for port B - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite from the register bit, an interrupt occurs.
    DEFVALB = 0x07
    # Interrupt control register for port A.  If 1 interrupt is fired when the
    # pin matches the default value, if 0 the interrupt is fired on state
    # change
    INTCONA = 0x08
    # Interrupt control register for port B.  If 1 interrupt is fired when the
    # pin matches the default value, if 0 the interrupt is fired on state
    # change
    INTCONB = 0x09
    IOCON = 0x0A  # see datasheet for configuration register
    GPPUA = 0x0C  # pull-up resistors for port A
    GPPUB = 0x0D  # pull-up resistors for port B
    # The INTF register reflects the interrupt condition on the port A pins of
    # any pin that is enabled for interrupts. A set bit indicates that the
    # associated pin caused the interrupt.
    INTFA = 0x0E
    # The INTF register reflects the interrupt condition on the port B pins of
    # any pin that is enabled for interrupts.  A set bit indicates that the
    # associated pin caused the interrupt.
    INTFB = 0x0F
    # The INTCAP register captures the GPIO port A value at the time the
    # interrupt occurred.
    INTCAPA = 0x10
    # The INTCAP register captures the GPIO port B value at the time the
    # interrupt occurred.
    INTCAPB = 0x11
    GPIOA = 0x12  # data port A
    GPIOB = 0x13  # data port B
    OLATA = 0x14  # output latches A
    OLATB = 0x15  # output latches B

    # variables
    # create a byte array for each port
    # index: 0 = Direction, 1 = value, 2 = pullup, 3 = polarity
    __port_a_direction = 0x00
    __port_b_direction = 0x00

    __port_a_value = 0x00
    __port_b_value = 0x00

    __port_a_pullup = 0x00
    __port_b_pullup = 0x00

    __port_a_polarity = 0x00
    __port_b_polarity = 0x00

    __ioaddress = 0x20  # I2C address
    __inta = 0x00  # interrupt control for port a
    __intb = 0x00  # interrupt control for port a
    # initial configuration - see IOCON page in the MCP23017 datasheet for
    # more information.
    __ioconfig = 0x22
    __helper = None
    __bus = None

    def __init__(self, address, bus):
        """
        init object with i2c address, default is 0x20, 0x21 for IOPi board,
        load default configuration
        """
        self.__ioaddress = address
        self.__bus = bus
        self.__bus.write_byte_data(
            self.__ioaddress, self.IOCON, self.__ioconfig)
        self.__port_a_value = self.__bus.read_byte_data(
            self.__ioaddress, self.GPIOA)
        self.__port_b_value = self.__bus.read_byte_data(
            self.__ioaddress, self.GPIOB)
        self.__bus.write_byte_data(self.__ioaddress, self.IODIRA, 0x00)
        self.__bus.write_byte_data(self.__ioaddress, self.IODIRB, 0x00)
        self.set_port_pullups(0, 0)
        self.set_port_pullups(1, 0)
        self.write_port(0, 0)
        self.write_port(1, 0)
        return

    # local methods
    def checkbit(self, byte, bit):
        """ internal method for reading the value of a single bit
        within a byte """
        value = 0
        if byte & (1 << bit):
            value = 1
        return value

    @staticmethod
    def __updatebyte(byte, bit, value):
        """
        internal method for setting the value of a single bit within a byte
        """
        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    # public methods

    def set_pin_direction(self, pin, direction):
        """
         set IO direction for an individual pin
         pins 1 to 16
         direction 1 = input, 0 = output
         """
        pin = pin - 1
        if pin < 8:
            self.__port_a_direction = self.__updatebyte(
                self.__port_a_direction, pin, direction)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRA, self.__port_a_direction)
        else:
            self.__port_b_direction = self.__updatebyte(
                self.__port_b_direction, pin - 8, direction)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRB, self.__port_b_direction)
        return

    def set_port_direction(self, port, direction):
        """
        set direction for an IO port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        1 = input, 0 = output
        """

        if port == 1:
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRB, direction)
            self.__port_b_direction = direction
        else:
            self.__bus.write_byte_data(
                self.__ioaddress, self.IODIRA, direction)
            self.__port_a_direction = direction
        return

    def set_pin_pullup(self, pin, value):
        """
        set the internal 100K pull-up resistors for an individual pin
        pins 1 to 16
        value 1 = enabled, 0 = disabled
        """
        pin = pin - 1
        if pin < 8:
            self.__port_a_pullup = self.__updatebyte(
                self.__port_a_pullup, pin, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPPUA, self.__port_a_pullup)
        else:
            self.__port_b_pullup = self.__updatebyte(
                self.__port_b_pullup, pin - 8, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPPUB, self.__port_b_pullup)
        return

    def set_port_pullups(self, port, value):
        """
        set the internal 100K pull-up resistors for the selected IO port
        """

        if port == 1:
            self.__port_b_pullup = value
            self.__bus.write_byte_data(self.__ioaddress, self.GPPUB, value)
        else:
            self.__port_a_pullup = value
            self.__bus.write_byte_data(self.__ioaddress, self.GPPUA, value)
        return

    def write_pin(self, pin, value):
        """
        write to an individual pin 1 - 16
        """
        pin = pin - 1
        if pin < 8:
            self.__port_a_value = self.__updatebyte(self.__port_a_value,
                                                    pin, value)
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOA,
                                       self.__port_a_value)
        else:
            pin = pin - 8
            self.__port_b_value = self.__updatebyte(self.__port_b_value,
                                                    pin, value)
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOB,
                                       self.__port_b_value)
        return

    def write_port(self, port, value):
        """
        write to all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 1:
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOB, value)
            self.__port_b_value = value
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOA, value)
            self.__port_a_value = value
        return

    def read_pin(self, pin):
        """
        read the value of an individual pin 1 - 16
        returns 0 = logic level low, 1 = logic level high
        """
        value = 0
        pin = pin - 1
        if pin < 8:
            self.__port_a_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOA)
            value = self.checkbit(self.__port_a_value, pin)
        else:
            pin = pin - 8
            self.__port_b_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOB)
            value = self.checkbit(self.__port_b_value, pin)
        return value

    def read_port(self, port):
        """
        read all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        returns number between 0 and 255 or 0x00 and 0xFF
        """
        value = 0
        if port == 1:
            self.__port_b_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOB)
            value = self.__port_b_value
        else:
            self.__port_a_value = self.__bus.read_byte_data(
                self.__ioaddress, self.GPIOA)
            value = self.__port_a_value
        return value

    def invert_port(self, port, polarity):
        """
        invert the polarity of the pins on a selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """

        if port == 1:
            self.__bus.write_byte_data(self.__ioaddress, self.IPOLB, polarity)
            self.__port_b_polarity = polarity
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.IPOLA, polarity)
            self.__port_a_polarity = polarity
        return

    def invert_pin(self, pin, polarity):
        """
        invert the polarity of the selected pin
        pins 1 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """

        pin = pin - 1
        if pin < 8:
            self.__port_a_polarity = self.__updatebyte(
                self.__port_a_polarity,
                pin,
                polarity)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IPOLA, self.__port_a_polarity)
        else:
            self.__port_b_polarity = self.__updatebyte(
                self.__port_b_polarity,
                pin - 8,
                polarity)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IPOLB, self.__port_b_polarity)
        return

    def mirror_interrupts(self, value):
        """
        1 = The INT pins are internally connected, 0 = The INT pins are not
        connected. __inta is associated with PortA and __intb is associated
        with PortB
        """

        if value == 0:
            self.__ioconfig = self.__updatebyte(self.__ioconfig, 6, 0)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        if value == 1:
            self.__ioconfig = self.__updatebyte(self.__ioconfig, 6, 1)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        return

    def set_interrupt_polarity(self, value):
        """
        This sets the polarity of the INT output pins
        1 = Active-high.
        0 = Active-low.
        """

        if value == 0:
            self.__ioconfig = self.__updatebyte(self.__ioconfig, 1, 0)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        if value == 1:
            self.__ioconfig = self.__updatebyte(self.__ioconfig, 1, 1)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__ioconfig)
        return

    def set_interrupt_type(self, port, value):
        """
        Sets the type of interrupt for each pin on the selected port
        1 = interrupt is fired when the pin matches the default value, 0 =
        the interrupt is fired on state change
        """

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.INTCONA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.INTCONB, value)
        return

    def set_interrupt_defaults(self, port, value):
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite from the register bit, an
        interrupt occurs.
        """

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.DEFVALA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.DEFVALB, value)
        return

    def set_interrupt_on_port(self, port, value):
        """
        Enable interrupts for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.GPINTENA, value)
            self.__inta = value
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPINTENB, value)
            self.__intb = value
        return

    def set_interrupt_on_pin(self, pin, value):
        """
        Enable interrupts for the selected pin
        Pin = 1 to 16
        Value 0 = interrupt disabled, 1 = interrupt enabled
        """

        pin = pin - 1
        if pin < 8:
            self.__inta = self.__updatebyte(self.__inta, pin, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPINTENA, self.__inta)
        else:
            self.__intb = self.__updatebyte(self.__intb, pin - 8, value)
            self.__bus.write_byte_data(
                self.__ioaddress, self.GPINTENB, self.__intb)
        return

    def read_interrupt_status(self, port):
        """
        read the interrupt status for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        value = 0
        if port == 0:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTFA)
        else:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTFB)
        return value

    def read_interrupt_capture(self, port):
        """
        read the value from the selected port at the time of the last
        interrupt trigger
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """
        value = 0
        if port == 0:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTCAPA)
        else:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTCAPB)
        return value

    def reset_interrupts(self):
        """
        Reset the interrupts A and B to 0
        """

        self.read_interrupt_capture(0)
        self.read_interrupt_capture(1)
        return
