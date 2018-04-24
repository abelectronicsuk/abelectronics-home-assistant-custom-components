# Home Assistant components for Raspberry Pi expansion boards from ABElectronics UK

Software interfaces for Home Assistant from [home-assistant.io](https://home-assistant.io/) to use with Raspbery Pi expanstion boards from [www.abelectronics.co.uk](https://www.abelectronics.co.uk/)

## ADC Pi Plus and ADC Pi Zero
The **adcpi** directory contains sample code and interface custom component to allow Home Assistant to communicate with the ADC Pi, ADC Pi Plus and ADC Pi Zero from AB Electronics UK.

## IO Pi Plus and ADC Pi Zero Custom Components
The **iopi** directory contains a binary_sensor component and sensor component which  communicates with the IO Pi Plus and IO Pi Zero from AB Electronics UK to use with Home Assistant and Hass.io releases.

## IO Pi Plus and IO Pi Zero CLI C Interface
The **iopi-using-cli** directory contains sample code and interface application to allow Home Assistant to communicate with the IO Pi Plus and IO Pi Zero from AB Electronics UK using the C IOPi CLI application.
### Please note that the CLI C interface will not run on the Hass.io version due to permissions restrictions to the I2C port.


## IO Pi CLI Application
The **iopi-cli-app** directory contains a command line interface application written in C which  communicates with the IO Pi Plus and IO Pi Zero from AB Electronics UK. Full source code is provided.

## License
MIT