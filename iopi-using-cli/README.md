# Home Assistant component for IO Plus & Zero Raspberry Pi expansion boards using CLI interface software

Software interfaces for Home Assistant from [home-assistant.io](https://home-assistant.io/) to use with Raspbery Pi expanstion boards from [www.abelectronics.co.uk](https://www.abelectronics.co.uk/) using CLI interface software.

This has been tested on a Raspberry Pi using manual installation of Home Assistance from [home-assistant.io/docs/installation/raspberry-pi](https://home-assistant.io/docs/installation/raspberry-pi/_).

### Please note that the CLI interface will not run on the Hass.io version due to permissions restrictions to the I2C port. 

Provides:

- Functionality to read and write to IO pins on [IO Pi Plus](https://www.abelectronics.co.uk/p/54/IO-Pi-Plus) and [IO Pi Zero](https://www.abelectronics.co.uk/p/71/IO-Pi-Zero)

## Installation for IO Pi Plus and Zero

```
Copy /iopi to the root of the Home Assistant config directory
```
The path '/home/homeassistant/.homeassistant/' in the following code will need to be updated to the correct path of your homeassistant installation.

The IO Pi can be configured with each pin as either an input or output. For Home Assistance the input mode needs to be setup using binary sensors. 

## Sensor / Input Mode Configuration
The following code sets pins 1 to 8 as inputs on chip address 0x20.

The IOPi input pins can be configured with the following code either in configuration.yaml or binary_sensors.ymal:

```yaml
- platform: command_line
  name: iopi_input_one
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 1 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1

- platform: command_line    
  name: iopi_input_two
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 2 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  friendly_name: IO Pi 2
  scan_interval: 1

- platform: command_line
  name: iopi_input_three
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 3 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1  

- platform: command_line
  name: iopi_input_four
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 4 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1 

- platform: command_line
  name: iopi_input_five
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 5 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1 

- platform: command_line
  name: iopi_input_six
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 6 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1  

- platform: command_line
  name: iopi_input_seven
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 7 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1 

- platform: command_line
  name: iopi_input_eight
  command: '/home/homeassistant/.homeassistant/./iopi -a 0x20 -u 1 -n 8 -d 1 -r -i 1'
  device_class: power
  payload_on: 1
  payload_off: 0
  scan_interval: 1  
```

## Switch / Output Mode Configuration
The following code sets pins 1 to 8 as outputs on chip address 0x21.

The IOPi output pins can be configured with the following code either in configuration.yaml or switches.ymal:

```yaml
- platform: command_line
  switches:
    iopi_pin_one:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 1 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 1 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 1 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 1
    iopi_pin_two:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 2 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 2 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 2 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 2
    iopi_pin_three:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 3 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 3 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 3 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 3
    iopi_pin_four:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 4 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 4 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 4 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 4
    iopi_pin_five:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 5 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 5 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 5 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 5
    iopi_pin_six:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 6 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 6 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 6 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 6
    iopi_pin_seven:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 7 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 7 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 7 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 7
    iopi_pin_eight:
      command_on: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 8 -d 0 -w 1'
      command_off: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 8 -d 0 -w 0'
      command_state: '/home/homeassistant/.homeassistant/./iopi -a 0x21 -n 8 -d 0 -r'
      value_template: '{{ value == "1" }}'
      friendly_name: IO Pi 8     
```

## Configuration Parameters

The iopi software uses the following command arguments:

```
  -a --address=i2c address; e.g., '-a 0x21' sets the I2C address to 0x21; The default address if -a is not specified is 0x20

-p --port=value; set the port to access; e.g., '-p 1' or '--port=1' sets the port to 1. If no port or pin is specified the program will default to port 0 -n --pin=value; set the pin to access; e.g., '-n 7' or '--pin=7' sets the pin to 7. If no port or pin is specified the program will default to port 0. If a port is specified as well as a pin the program will use the selected port and ignore the pin value.

-r --read; Read the status of the selected port or pin; For each pin 0 = logic low, 1 = logic high; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1.

-w --write=value; Write a value to the selected port or pin; For each pin 0 = logic low, 1 = logic high; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-w 1 -n 3' will set pin 3 to be logic high.

-d --direction=value; set port or pin direction; For each pin 0 = output, 1 = input; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-d 1 -n 3' will set pin 3 to be an input.

-i --invert=value; invert the selected port or pin; For each pin 0 = normal, 1 = inverted; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-i 1 -n 3' will set pin 3 to be inverted.

-u --pullup=value; Set the internal 100K pull-up resistors for the selected port or pin; 1 = enabled, 0 = disabled; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-u 1 -n 3' will enable the pull-up resistor for pin 3.

-m --mirrorinterrupts=value; Set the interrupt pins to be mirrored or for separate ports; 1 = The pins are internally connected, 0 = The pins are not connected. INTA is associated with PortA and INTB is associated with PortB; e.g., '-m 1' will set both interrupt pins IA and IB to be mirrored.

-l --interruptpolarity=value; Set the polarity of the interrupt output pins IA and IB; 1 = Active-high, 0 = Active-low; ; e.g., '-l 1' will set the interrupt output pins to go logic high when an interrupt occurs.

-t --interrupttype=value; Sets the type of interrupt for the selected pin or port; 1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-t 0 -n 3' will set the interrupt for pin 3 to trigger on state change.

-f --interruptdefaults=value; Set the compare value for interrupt-on-change on the selected port. If the associated pin level is the opposite from the set value an interrupt occurs; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-f 1 -n 3' will set the default value for pin 3 to be logic high.

-e --enableinterrupts=value; Enable interrupts for the selected port or pin; For each pin 0 = off, 1 = on; If a port has been selected the value can be 0 to 255. If a pin has been selected the value can be 0 or 1; e.g., '-e 1 -n 3' will enable the interrupt for pin 3.

-s --interruptstatus; Read the interrupt status for the selected port or pin

-c --interruptcapture; Read the value from the selected port or pin at the time of the last interrupt trigger

-z --resetinterrupts; Set the interrupts IA and IB to 0

-h --help; Display a list of available options

-b --binary; Set the output number format to binary; e.g., 0b00100100

-x --hex; Set the output number format to hexidecimal; e.g., 0xFC
```