# Home Assistant components for Raspberry Pi expansion boards from AB Electronics UK

[![Project Maintenance][maintenance-shield]][user_profile]

[![Community Forum][forum-shield]](https://www.abelectronics.co.uk/forums/)

Software interfaces for Home Assistant from [home-assistant.io](https://home-assistant.io/) to use with Raspbery Pi expansion boards from [www.abelectronics.co.uk](https://www.abelectronics.co.uk/)

## Requirements

These components requires the I2C bus on the Raspberry Pi to be enabled.

If you are using the Home Assistant Operating System you can’t use existing methods to enable the I2C bus on a Raspberry Pi, you will have to enable the I2C interface manually. Please follow the instruction on https://www.home-assistant.io/common-tasks/os#enable-i2c to enable I2C on your Home Assistant Operating System installation.

## ADC Differential Pi Custom Components
The **abelectronicsadcdifferentialpi** directory contains a sensor component which communicates with the [ADC Differential Pi](https://www.abelectronics.co.uk/p/65/adc-differential-pi-raspberry-pi-analogue-to-digital-converter) Raspberry Pi expansion board from AB Electronics UK to use with Home Assistant.

The ADC Differential Pi is an 8 channel 18 bit differential analogue to digital converter designed to work with the Raspberry Pi. The ADC Differential Pi is based on two Microchip MCP3424 A/D converters each containing 4 analogue inputs. 

ADC Input Voltage
-2.048V to +2.048V

## ADC Pi Custom Components
The **abelectronicsadcpi** directory contains a sensor component which communicates with the [ADC Pi](https://www.abelectronics.co.uk/p/69/adc-pi-raspberry-pi-analogue-to-digital-converter) Raspberry Pi expansion board from AB Electronics UK to use with Home Assistant.

The ADC Pi is an 8 channel 17 bit analogue to digital converter designed to work with the Raspberry Pi. The ADC Pi is based on two Microchip MCP3424 A/D converters each containing 4 analogue inputs. 

ADC Input Voltage
0V to +5.06V

## IO Pi Plus and IO Pi Zero Custom Components
The **abelectronicsiopi** directory contains a binary_sensor component and switch component which  communicates with the [IO Pi Plus](https://www.abelectronics.co.uk/p/54/io-pi-plus) and [IO Pi Zero](https://www.abelectronics.co.uk/p/71/io-pi-zero) Raspberry Pi expansion boards from AB Electronics UK to use with Home Assistant.

The IO Pi Plus is a 32 channel digital expansion board designed for use on the Raspberry Pi. The board is based around the MCP23017 16-bit I/O expander from Microchip Technology Inc. A pair of MCP23017 expanders are included on the board allowing you to connect up to 32 digital inputs or outputs to the Raspberry Pi.  The IO Pi Plus is powered through the host Raspberry Pi using the GPIO port and extended pins on the GPIO connector allow you to stack the IO Pi Plus along with other expansion boards.

The I2C address bits are selectable using the on-board solder jumpers. The MCP23017 supports up to 8 different I2C addresses so with two MCP23017 devices on each IO Pi you can stack up to 4 IO Pi boards on a single Raspberry Pi giving a maximum of 128 I/O ports.

The IO Pi Zero is a 16 channel digital expansion board designed for use on the Raspberry Pi Zero. 

## License

Distributed under the MIT License. See `LICENSE` for more information.


[license-shield]: https://img.shields.io/github/license/abelectronicsuk/abelectronicsiopi.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40abelectronicsuk-blue.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[user_profile]: https://github.com/abelectronicsuk