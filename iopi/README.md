# Home Assistant components for IO Plus & Zero Raspberry Pi expansion boards using Custom Components folders

Software interfaces for Home Assistant from [home-assistant.io](https://home-assistant.io/) to use with IO Pi Plus/Zero MCP23017 based Raspbery Pi expanstion boards from [www.abelectronics.co.uk](https://www.abelectronics.co.uk/) using binary sensor and switch components.

This has been tested on a Raspberry Pi using manual installation of Home Assistance from [home-assistant.io/docs/installation/raspberry-pi](https://home-assistant.io/docs/installation/raspberry-pi/_) and with Hass.io installation from [home-assistant.io/hassio](https://home-assistant.io/hassio/)


Provides:

- Functionality to read and write to IO pins on [IO Pi Plus](https://www.abelectronics.co.uk/p/54/IO-Pi-Plus) and [IO Pi Zero](https://www.abelectronics.co.uk/p/71/IO-Pi-Zero) boards which use the MCP23017 I2C port expander.

## Installation for IO Pi Plus and Zero

```
Copy /custom_components folder to the root of the Home Assistant config directory
```
The iopiinputssensor.py file located in the binary_sensor directory allows you to read from the 16 IO ports on the MCP23017 IC using the Binary Sensor platform in Home Assistant.

The iopiswitch.py file located in the switch  directory allows you to write to the 16 IO ports on the MCP23017 IC using the switch platform in Home Assistant.


## Binary Sensor / Input Mode Configuration
The following code uses the iopiinputssensor.py binary sensor file to read the inputs on chip address 0x20.

The IOPi input pin status can be configured with the following code either in configuration.yaml or binary_sensors.ymal.

```yaml
- platform: iopiinputssensor
  name: IOPiInputs
  i2c_address: 0x20
  pullup: 1
  scan_interval: 1
```
## Configuration variables:

* **name** (Required): Name that will be used in the sensor.
* **i2c_address** (Required): The I2C address of the MCP23017 IC.
* **pullup** (Required): Setting the pullup value to 1 will enable the internal pullup resistors in the MCP23017 IC. A value of 0 (zero) will disable the internal pullup resistors.

The pin status is held in attributes which are named pin1 to pin16 and can be added to the Home Assistance user interface with the following template which needs to be added to configuration.yaml or binary_sensors.ymal.

```yaml
- platform: template
  sensors:
    iopi_in1:
      value_template: '{{states.binary_sensor.iopi.attributes.pin1 == 1}}'
      friendly_name: 'IO input 1'
    iopi_in2:
      value_template: '{{states.binary_sensor.iopi.attributes.pin2 == 1}}'
      friendly_name: 'IO input 2'  
    iopi_in3:
      value_template: '{{states.binary_sensor.iopi.attributes.pin3 == 1}}'
      friendly_name: 'IO input 3'
    iopi_in4:
      value_template: '{{states.binary_sensor.iopi.attributes.pin4 == 1}}'
      friendly_name: 'IO input 4'
    iopi_in5:
      value_template: '{{states.binary_sensor.iopi.attributes.pin5 == 1}}'
      friendly_name: 'IO input 5'
    iopi_in6:
      value_template: '{{states.binary_sensor.iopi.attributes.pin6 == 1}}'
      friendly_name: 'IO input 6' 
    iopi_in7:
      value_template: '{{states.binary_sensor.iopi.attributes.pin7 == 1}}'
      friendly_name: 'IO input 7'  
    iopi_in8:
      value_template: '{{states.binary_sensor.iopi.attributes.pin8 == 1}}'
      friendly_name: 'IO input 8' 
    iopi_in9:
      value_template: '{{states.binary_sensor.iopi.attributes.pin9 == 1}}'
      friendly_name: 'IO input 9'
    iopi_in10:
      value_template: '{{states.binary_sensor.iopi.attributes.pin10 == 1}}'
      friendly_name: 'IO input 10'  
    iopi_in11:
      value_template: '{{states.binary_sensor.iopi.attributes.pin11 == 1}}'
      friendly_name: 'IO input 11'
    iopi_in12:
      value_template: '{{states.binary_sensor.iopi.attributes.pin12 == 1}}'
      friendly_name: 'IO input 12'
    iopi_in13:
      value_template: '{{states.binary_sensor.iopi.attributes.pin13 == 1}}'
      friendly_name: 'IO input 13'
    iopi_in14:
      value_template: '{{states.binary_sensor.iopi.attributes.pin14 == 1}}'
      friendly_name: 'IO input 14' 
    iopi_in15:
      value_template: '{{states.binary_sensor.iopi.attributes.pin15 == 1}}'
      friendly_name: 'IO input 15'  
    iopi_in16:
      value_template: '{{states.binary_sensor.iopi.attributes.pin16 == 1}}'
      friendly_name: 'IO input 16'

```


## Switch / Output Mode Configuration
The following code uses the iopiswitch.py switch file to write to the chip on address 0x21.

The IOPi output pin status can be configured with the following code either in configuration.yaml or switches.ymal.

```yaml
- platform: iopiswitch
  i2c_address: 0x21
  name: IOSwitches
  invert_logic: False
  pins:
    1:
      name: Pin 1
      initial: True
    2:
      name: Pin 2
      initial: True
    3:
      name: Pin 3
    4:
      name: Pin 4 
    5:
      name: Pin 5
    6:
      name: Pin 6
    7:
      name: Pin 7
    8:
      name: Pin 8
    9:
      name: Pin 9
    10:
      name: Pin 10
    11:
      name: Pin 11
    12:
      name: Pin 12 
    13:
      name: Pin 13
    14:
      name: Pin 14
    15:
      name: Pin 15
    16:
      name: Pin 16
```
## Configuration variables:

* **name** (Required): Name that will be used in the sensor.
* **i2c_address** (Required): The I2C address of the MCP23017 IC.
* **invert_logic** (Optional): If `true`, inverts the output logic to ACTIVE LOW. Default: `false` (ACTIVE HIGH)
* **pins** (Required): This section will contain a list of the pins you wish to use as outputs.
  * **pin number** (Required): The pin number that corresponds with the pin number on the IOPi Plus/Zero 
  * **name** (Required): Name that will be used in the switch.
  * **initial** (Optional): The initial value for this port. Defaults to False 

## Example groups.yaml file
The following code can be used in the groups.yaml file to display data using the IO Pi Plus/Zero inputs and outputs.

```yaml
# REPLACE HOME PAGE
  default_view:
    name: Home
    view: yes
    icon: mdi:home
    entities:
      - group.iopioutputs
      - group.iopiinputs    
  
  mainview:
    view: no
    name: Overview
    
  iopiinputs:
    view: no
    name: IOPi Inputs
    control: hidden
    entities:
      - binary_sensor.iopi_in1
      - binary_sensor.iopi_in2
      - binary_sensor.iopi_in3
      - binary_sensor.iopi_in4
      - binary_sensor.iopi_in5
      - binary_sensor.iopi_in6
      - binary_sensor.iopi_in7
      - binary_sensor.iopi_in8
      - binary_sensor.iopi_in9
      - binary_sensor.iopi_in10
      - binary_sensor.iopi_in11
      - binary_sensor.iopi_in12
      - binary_sensor.iopi_in13
      - binary_sensor.iopi_in14
      - binary_sensor.iopi_in15
      - binary_sensor.iopi_in16
         
  iopioutputs:
    view: no
    name: IOPi Outputs
    control: hidden
    entities:
      - switch.pin_1
      - switch.pin_2
      - switch.pin_3
      - switch.pin_4
      - switch.pin_5
      - switch.pin_6
      - switch.pin_7
      - switch.pin_8
      - switch.pin_9
      - switch.pin_10
      - switch.pin_11
      - switch.pin_12
      - switch.pin_13
      - switch.pin_14
      - switch.pin_15
      - switch.pin_16

```