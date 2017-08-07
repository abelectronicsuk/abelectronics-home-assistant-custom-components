# Home Assistant component for ADC Pi Plus & Zero Raspberry Pi expansion boards

Software interfaces for Home Assistant from [home-assistant.io](https://home-assistant.io/) to use with Raspbery Pi expanstion boards from [www.abelectronics.co.uk](https://www.abelectronics.co.uk/)

Provides:

- Functionality to read voltages from [ADC Pi Plus](https://www.abelectronics.co.uk/p/56/ADC-Pi-Plus-Raspberry-Pi-Analogue-to-Digital-converter) and [ADC Pi Zero](https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter)

## Installation for ADC Pi Plus and Zero

```r
Copy /custom_components/sensor/adcpi.py to /custom_components/sensor/adcpi.py in Home Assistant config directory
```

## Sensor Configuration
The adcpi sensor can be configured with the following code either in configuration.yaml or sensors.ymal:

```yaml
- platform: adcpi
  name: ADCPi
  i2c_address: 0x68
  i2c_address2: 0x69
  pga: 1
  bitrate: 18
  scan_interval: 5
```

## Configuration Parameters

The adcpi uses the following parameters:

```
  i2c_address: xxxx - default I2C address: 0x68

  i2c_address2: xxxx - default I2C address: 0x69

  pga: x - Set the gain of the PGA on the chip. Parameters: gain - 1, 2, 4, 8

  bitrate: xx - Set the sample bit rate of the adc. 
    12 = 12 bit (240SPS max)
    14 = 14 bit (60SPS max)
    16 = 16 bit (15SPS max)
    18 = 18 bit (3.75SPS max)
```

## Usage

Add the following template to your configuration.yaml or sensors.ymal to display the data from the adcpi inputs:

```yaml
- platform: template
  sensors:
    adcinput1:
      value_template: '{{states.sensor.adcpi.attributes.input1}}'
      friendly_name: 'ADC input 1'
      unit_of_measurement: 'Volts'
    adcinput2:
      value_template: '{{states.sensor.adcpi.attributes.input2}}'
      friendly_name: 'ADC input 2'
      unit_of_measurement: 'Volts'
    adcinput3:
      value_template: '{{states.sensor.adcpi.attributes.input3}}'
      friendly_name: 'ADC input 3'
      unit_of_measurement: 'Volts'
    adcinput4:
      value_template: '{{states.sensor.adcpi.attributes.input4}}'
      friendly_name: 'ADC input 4'
      unit_of_measurement: 'Volts'
    adcinput5:
      value_template: '{{states.sensor.adcpi.attributes.input5}}'
      friendly_name: 'ADC input 5'
      unit_of_measurement: 'Volts'
    adcinput6:
      value_template: '{{states.sensor.adcpi.attributes.input6}}'
      friendly_name: 'ADC input 6'
      unit_of_measurement: 'Volts'
    adcinput7:
      value_template: '{{states.sensor.adcpi.attributes.input7}}'
      friendly_name: 'ADC input 7'
      unit_of_measurement: 'Volts'
    adcinput8:
      value_template: '{{states.sensor.adcpi.attributes.input8}}'
      friendly_name: 'ADC input 8'
      unit_of_measurement: 'Volts' 
```