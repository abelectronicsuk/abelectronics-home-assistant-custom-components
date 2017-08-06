#include <stdio.h>

// Error Message Definitions

#define ERROR_NO_ARGUMENTS "no arguments given - run 'iopi -h' for help"


// help output

char helppage[]="\033[1m-a --address value\033[0m\te.g., '-a 0x21' sets the I2C address to 0x21.  The default address if -a is not specified is 0x20 \n\n\
\033[1m-p, --port value\033[0m\tset the port to access.  e.g., '-p 1' or '--port=1' sets the port to 1.  If no port or pin is specified the program will default to port 0\n\n\
\033[1m-n, --pin value\033[0m\tset the pin to access.  e.g., '-n 7' or '--pin=7' sets the pin to 7.  If no port or pin is specified the program will default to port 0.  If a port is specified as well as a pin the program will use the selected port and ignore the pin value.\n\n\
\033[1m-r, --read\033[0m\tRead the status of the selected port or pin.  For each pin 0 = logic low, 1 = logic high.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.\n\n\
\033[1m-w, --write value\033[0m\tWrite a value to the selected port or pin.  For each pin 0 = logic low, 1 = logic high.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.   e.g., '-w 1 -n 3' will set pin 3 to be logic high.\n\n\
\033[1m-d, --direction value\033[0m\tset port or pin direction.  For each pin 0 = output, 1 = input.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.   e.g., '-d 1 -n 3' will set pin 3 to be an input.  \n\n\
\033[1m-i, --invert value\033[0m\tInvert the selected port or pin.  For each pin 0 = normal, 1 = inverted.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.   e.g., '-i 1 -n 3' will set pin 3 to be inverted.\n\n\
\033[1m-u, --pullup value\033[0m\tSet the internal 100K pull-up resistors for the selected port or pin.  1 = enabled, 0 = disabled.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.   e.g., '-u 1 -n 3' will enable the pull-up resistor for pin 3.\n\n\
\033[1m-m, --mirrorinterrupts value\033[0m\tSet the interrupt pins to be mirrored or for separate ports.  1 = The pins are internally connected, 0 = The pins are not connected. INTA is associated with PortA and INTB is associated with PortB.   e.g., '-m 1' will set both interrupt pins IA and IB to be mirrored.\n\n\
\033[1m-l, --interruptpolarity value\033[0m\tSet the polarity of the interrupt output pins IA and IB.  1 = Active-high, 0 = Active-low.  .  e.g., '-l 1' will set the interrupt output pins to go logic high when an interrupt occurs.\n\n\
\033[1m-t, --interrupttype value\033[0m\tSets the type of interrupt for the selected pin or port.  1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.  e.g., '-t 0 -n 3' will set the interrupt for pin 3 to trigger on state change.\n\n\
\033[1m-f, --interruptdefault value\033[0m\tSet the compare value for interrupt-on-change on the selected port. If the associated pin level is the opposite from the set value an interrupt occurs.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.   e.g., '-f 1 -n 3' will set the default value for pin 3 to be logic high.\n\n\
\033[1m-e, --enableinterrupts value\033[0m\tEnable interrupts for the selected port or pin.  For each pin 0 = off, 1 = on.  If a port has been selected the value can be 0 to 255.  If a pin has been selected the value can be 0 or 1.   e.g., '-e 1 -n 3' will enable the interrupt for pin 3.\n\n\
\033[1m-s, --interruptstatus\033[0m\tRead the interrupt status for the selected port or pin\n\n\
\033[1m-c, --interruptcapture\033[0m\tRead the value from the selected port or pin at the time of the last interrupt trigger\n\n\
\033[1m-z, --resetinterrupts\033[0m\tSet the interrupts IA and IB to 0\n\n\
\033[1m-h, --help\033[0m\tDisplay a list of available options\n\n\
\033[1m-b, --binary\033[0m\tSet the output number format to binary.  e.g., 0b00100100\n\n\
\033[1m-x, --hex\033[0m\tSet the output number format to hexidecimal.  e.g., 0xFC";

void display_help(){
    

    printf(helppage);
}