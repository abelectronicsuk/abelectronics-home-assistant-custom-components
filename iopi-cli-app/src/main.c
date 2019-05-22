#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include "abe_iopi.h"
#include "main.h"
#include "help.h"

// Error Message Definitions
#define ERROR_NO_ARGUMENTS "no arguments given - run 'iopi -h' for help"
#define ERROR_PARAM_ADDRESS "Error: -a and --address require a parameter of 0x20 to 0x27. e.g., -a 0x21 \n"
#define ERROR_PARAM_PORT "Error: -p and --port require a parameter of 0 or 1.  e.g., -p 1 \n"
#define ERROR_PARAM_PIN "Error: -n and --pin require a parameter of 1 to 16.  e.g., -n 3 \n"
#define ERROR_PARAM_WRITE "Error: -w and --write require a parameter.  e.g., -w 1 \n"
#define ERROR_PARAM_DIRECTION "Error: -d and --direction require a parameter.  e.g., -d 1 \n"
#define ERROR_PARAM_INVERT "Error: -i and --invert require a parameter.  e.g., -i 1 \n"
#define ERROR_PARAM_PULLUP "Error: -u and --pullup require a parameter.  e.g., -u 1 \n"
#define ERROR_PARAM_INTERRUPTPOLARITY "Error: -l and --interruptpolarity require a parameter.  e.g., -l 1 \n"
#define ERROR_PARAM_MIRRORINTERRUPTS "Error: -m and --mirrorinterrupts require a parameter.  e.g., -m 1 \n"
#define ERROR_PARAM_INTERRUPTTYPE "Error: -t and --interrupttype require a parameter.  e.g., -t 1 \n"
#define ERROR_PARAM_INTERRUPTDEFAULTS "Error: -f and --interruptdefaults require a parameter.  e.g., -f 1 \n"
#define ERROR_PARAM_ENABLEINTERRUPTS "Error: -e and --enableinterrupts require a parameter.  e.g., -e 1 \n"


// global variables

struct options
{
  char address;
  char port;
  char pin;
  char read;
  char write;
  char direction;
  char invert;
  char pullup;
  char mirrorinterrupts;
  char interruptpolarity;
  char interrupttype;
  char interruptdefaults;
  char enableinterrupts;
  char interruptstatus;
  char interruptcapture;
  char resetinterrupts;
};


struct options flags = { 0 };
struct options param_values = { 0 };
struct options output_values = { 0 };

char output_format = 0; // 0 = dec, 1 = hex, 2 = bin
char output_count = 0;
char param_error = 0;

int main(int argc, char **argv)
{

  setvbuf(stdout, NULL, _IONBF, 0); // needed to print to the command line

  // set default i2c address
  param_values.address = 0x20;

  if (argc > 1)
  {
    int index = 0;

    // loop through the arguments and find any options beginning with -
    for (index = 0; index < argc; index++)
    {
      if (argv[index][0] == '-')
      {

        if ((index + 1) >= argc) // check if the option is the last argument
        { 
          parse_option(&argv[index], NULL);
        }
        else
        {
          if (argv[index + 1][0] != '-')
          { // option has a parameter
            parse_option(&argv[index], &argv[index] + 1);
          }
          else
          {
            parse_option(&argv[index], NULL);
          }
        }
      }
    }

    // check if the parameters were valid
    if (param_error == 0){
      // initialise the io pi and run the requested commands
      IOPi_init(param_values.address);
      run_io_commands();
      write_output();
    }
    else{
      exit(EXIT_FAILURE);
    }
  }
  else
  {
    printf(ERROR_NO_ARGUMENTS);
  }
  return 0;
}

void parse_option(char **option, char **parameter)
{
  // parse the argument to see if it is a valid option

  // i2c address
  if ((strcmp(*option, "-a") == 0) || (strcmp(*option, "--address") == 0)) 
  {
      if (parse_parameter(parameter, &param_values.address)){
        if (param_values.address < 0x20 || param_values.address > 0x27){
          printf(ERROR_PARAM_ADDRESS);
          exit(EXIT_FAILURE);
        }
      }
      else{printf(ERROR_PARAM_ADDRESS); param_error = 1;}      
  }

  // port
  else if (strcmp(*option, "-p") == 0 || strcmp(*option, "--port") == 0) 
  {
      if (parse_parameter(parameter, &param_values.port)){
        if (param_values.port == 0 || param_values.port == 1){
          flags.port = 1; 
        }
        else{
          printf(ERROR_PARAM_PORT); param_error = 1;
        }
      }
      else{printf(ERROR_PARAM_PORT); param_error = 1;}
  }

  // pin
  else if (strcmp(*option, "-n") == 0 || strcmp(*option, "--pin") == 0)
  {
      if (parse_parameter(parameter, &param_values.pin)){ 
        if (param_values.pin > 0 && param_values.pin < 17){
          flags.pin = 1; 
        }
        else{
          printf(ERROR_PARAM_PIN); param_error = 1;
        }
      }
      else{printf(ERROR_PARAM_PIN); param_error = 1;}
  }

  // read
  else if (strcmp(*option, "-r") == 0 || strcmp(*option, "--read") == 0)
  {
      flags.read = 1;
  }

  // write value
  else if (strcmp(*option, "-w") == 0 || strcmp(*option, "--write") == 0)
  {
      if (parse_parameter(parameter, &param_values.write)){ flags.write = 1; }
      else{printf(ERROR_PARAM_WRITE); param_error = 1;}
  }

  // direction value
  else if (strcmp(*option, "-d") == 0 || strcmp(*option, "--direction") == 0)
  {
      if (parse_parameter(parameter, &param_values.direction)){ flags.direction = 1; }
      else{printf(ERROR_PARAM_DIRECTION); param_error = 1;}
  }

  // invert
  else if (strcmp(*option, "-i") == 0 || strcmp(*option, "--invert") == 0)
  {
      if (parse_parameter(parameter, &param_values.invert)){ flags.invert = 1; }
      else{printf(ERROR_PARAM_INVERT); param_error = 1;}
  }

  // pullup
  else if (strcmp(*option, "-u") == 0 || strcmp(*option, "--pullup") == 0)
  {
      if (parse_parameter(parameter, &param_values.pullup)){ flags.pullup = 1; }
      else{printf(ERROR_PARAM_PULLUP); param_error = 1;}
  }

  // mirror interrupts
  else if (strcmp(*option, "-m") == 0 || strcmp(*option, "--mirrorinterrupts") == 0)
  {
      if (parse_parameter(parameter, &param_values.mirrorinterrupts)){ flags.mirrorinterrupts = 1; }
      else{printf(ERROR_PARAM_MIRRORINTERRUPTS); param_error = 1;}
  }

  // interrupt polarity
  else if (strcmp(*option, "-l") == 0 || strcmp(*option, "--interruptpolarity") == 0)
  {
      if (parse_parameter(parameter, &param_values.interruptpolarity)){ flags.interruptpolarity = 1; }
      else{printf(ERROR_PARAM_INTERRUPTPOLARITY); param_error = 1;}
  }

  // interrupt type
  else if (strcmp(*option, "-t") == 0 || strcmp(*option, "--interrupttype") == 0)
  {
      if (parse_parameter(parameter, &param_values.interrupttype)){ flags.interrupttype = 1; }
      else{printf(ERROR_PARAM_INTERRUPTTYPE); param_error = 1;}
  }

  // interrupt defaults
  else if (strcmp(*option, "-f") == 0 || strcmp(*option, "--interruptdefaults") == 0)
  {
      if (parse_parameter(parameter, &param_values.interruptdefaults)){ flags.interruptdefaults = 1; }
      else{printf(ERROR_PARAM_INTERRUPTDEFAULTS); param_error = 1;}
  }

  // enable interrupts
  else if (strcmp(*option, "-e") == 0 || strcmp(*option, "--enableinterrupts") == 0)
  {
      if (parse_parameter(parameter, &param_values.enableinterrupts)){ flags.enableinterrupts = 1; }
      else{printf(ERROR_PARAM_ENABLEINTERRUPTS); param_error = 1;}
  }

  // interrupt status
  else if (strcmp(*option, "-s") == 0 || strcmp(*option, "--interruptstatus") == 0)
  {
      flags.interruptstatus = 1;
  }

  // interrupt capture
  else if (strcmp(*option, "-c") == 0 || strcmp(*option, "--interruptcapture") == 0)
  {
      flags.interruptcapture = 1;
  }

  // reset interrupts
  else if (strcmp(*option, "-z") == 0 || strcmp(*option, "--resetinterrupts") == 0)
  {
      flags.resetinterrupts = 1;
  }

  // help
  else if (strcmp(*option, "-h") == 0 || strcmp(*option, "--help") == 0)
  {
      display_help();
  }

  // binary format
  else if (strcmp(*option, "-b") == 0 || strcmp(*option, "--binary") == 0)
  {
      output_format = 2;     
  } 

  // binary format
  else if (strcmp(*option, "-x") == 0 || strcmp(*option, "--hex") == 0)
  {
      output_format = 1;     
  }  

  /* more else if clauses */
  else /* default: */
  {
    printf("%s argument not recognised. Use -h or --help for a list of options. \n", *option);
    param_error = 1;
  }
}

bool parse_parameter(char **parameter, char *target)
{
  //
  // Parse the option parameter
  //
  if (parameter != NULL){
    long number = 999;

    // check the number base
    if ((strncmp(*parameter, "0x", 2) == 0)){ // hex value
        number = strtol(*parameter, NULL, 16);
    } 
    else if ((strncmp(*parameter, "0b", 2) == 0)){ // binary value
        char* p = *parameter + 2;
        number = strtol(p, NULL, 2);
    }
    else{ // assume it is a decimal value
        number = strtol(*parameter, NULL, 10);
    }
    // check for an error
    if (errno == ERANGE || number < 0 || number > 255){
        errno = 0;
        return false; // return error number
    }
    else{      
        *target = (char)number;
        return true; 
    }
  }
  else{
    return false;
  }  
}


void run_io_commands()
{
  // port
  if (flags.port == 1){ // check if the port value is vaid
    if (param_values.port < 0  || param_values.port > 1){
      printf("Port value outside of range 0 or 1\n");
      exit(EXIT_FAILURE);
    }
  }

  // pin  
  if (flags.pin == 1){ // check if the pin value is vaid
    if (flags.port == 0){
      if (param_values.pin < 1  || param_values.pin > 16){
        printf("Pin value outside of range 1 to 16\n");
        exit(EXIT_FAILURE);
      }
    }
    else{
      flags.pin = 0;
    }
  }

  // direction
  if (flags.direction == 1){ // check if the direction value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.direction >= 0 && param_values.direction <= 1){
          set_pin_direction(param_values.address, param_values.pin, param_values.direction);
        }
        else{
          printf("Direction value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      set_port_direction(param_values.address, param_values.port, param_values.direction);
    }
  }

  // invert
  if (flags.invert == 1){ // check if the invert value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.invert >= 0 && param_values.invert <= 1){
          invert_pin(param_values.address, param_values.pin, param_values.invert);
        }
        else{
          printf("Invert value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      invert_port(param_values.address, param_values.port, param_values.invert);
    }
  }

  // pullup
  if (flags.pullup == 1){ // check if the pullup value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.pullup >= 0 && param_values.pullup <= 1){
          set_pin_pullup(param_values.address, param_values.pin, param_values.pullup);
        }
        else{
          printf("Pullup value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      set_port_pullups(param_values.address, param_values.port, param_values.pullup);
    }
  }

  // write
  if (flags.write == 1){ // check if the write value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.write >= 0 && param_values.write <= 1){
          write_pin(param_values.address, param_values.pin, param_values.write);
        }
        else{
          printf("Write value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      write_port(param_values.address, param_values.port, param_values.write);
    }
  }

  // read 
  if (flags.read == 1){ // check if the read value is vaid
    if (flags.pin == 1){ // read pin
        output_values.read = read_pin(param_values.address, param_values.pin);
        output_count += 1;
    }
    else{ // read port
      output_values.read = read_port(param_values.address, param_values.port);
      output_count += 1;
    }
  }
  
  // enableinterrupts
  if (flags.enableinterrupts == 1){ // check if the enableinterrupts value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.enableinterrupts >= 0 && param_values.enableinterrupts <= 1){
          set_interrupt_on_pin(param_values.address, param_values.pin, param_values.enableinterrupts);
        }
        else{
          printf("enableinterrupts value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      set_interrupt_on_port(param_values.address, param_values.port, param_values.enableinterrupts);
    }
  }

  // mirrorinterrupts
  if (flags.mirrorinterrupts == 1){ // check if the mirrorinterrupts value is vaid
    if (param_values.mirrorinterrupts >= 0 && param_values.mirrorinterrupts <= 1){
      mirror_interrupts(param_values.address, param_values.mirrorinterrupts);
    }
    else{
    printf("mirrorinterrupts value outside of range 0 or 1\n");
       exit(EXIT_FAILURE);
    }
  }

  // interruptpolarity
  if (flags.interruptpolarity == 1){ // check if the interruptpolarity value is vaid
    if (param_values.interruptpolarity >= 0 && param_values.interruptpolarity <= 1){
      set_interrupt_polarity(param_values.address, param_values.interruptpolarity);
    }
    else{
      printf("interruptpolarity value outside of range 0 or 1\n");
      exit(EXIT_FAILURE);
    }
  }

  // interrupttype
  if (flags.interrupttype == 1){ // check if the interrupttype value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.interrupttype >= 0 && param_values.interrupttype <= 1){
          set_interrupt_type_on_pin(param_values.address, param_values.pin, param_values.interrupttype);
        }
        else{
          printf("interrupttype value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      set_interrupt_type(param_values.address, param_values.port, param_values.interrupttype);
    }
  }

  // interruptdefaults
  if (flags.interruptdefaults == 1){ // check if the interruptdefaults value is vaid
    if (flags.pin == 1){ // set pin
        if (param_values.interruptdefaults >= 0 && param_values.interruptdefaults <= 1){
          set_interrupt_defaults_on_pin(param_values.address, param_values.pin, param_values.interruptdefaults);
        }
        else{
          printf("interruptdefaults value outside of range 0 or 1\n");
          exit(EXIT_FAILURE);
        }
    }
    else{ // set port
      set_interrupt_defaults(param_values.address, param_values.port, param_values.interruptdefaults);
    }
  }
  
  // interruptstatus
  if (flags.interruptstatus == 1){ // check if the interruptstatus value is vaid
    if (flags.pin == 1){ // read pin
        output_values.interruptstatus = read_interrupt_status_on_pin(param_values.address, param_values.pin);
        output_count += 1;
    }
    else{ // read port
      output_values.interruptstatus = read_interrupt_status(param_values.address, param_values.port);
      output_count += 1;
    }
  }

  // interruptcapture
  if (flags.interruptcapture == 1){ // check if the interruptcapture value is vaid
    if (flags.pin == 1){ // read pin
        output_values.interruptcapture = read_interrupt_capture_on_pin(param_values.address, param_values.pin);
        output_count += 1;
    }
    else{ // read port
      output_values.interruptcapture = read_interrupt_capture(param_values.address, param_values.port);
      output_count += 1;
    }
  }

  // resetinterrupts
  if (flags.resetinterrupts == 1){ // check if the resetinterrupts value is vaid
    reset_interrupts(param_values.address);
  }

}

void write_output(){
  // write the output alone for a single value or json formatted for multiple values
  if (flags.read == 1){
      if (flags.interruptstatus == 1 || flags.interruptcapture == 1){
        printf("\"read\":\"%s\"", format_output(output_values.read));
      }
      else{
        printf("%s", format_output(output_values.read));
      }
  }
  if (flags.interruptstatus == 1){
      if (flags.read == 1 || flags.interruptcapture == 1){
        printf(",\"interruptstatus\":\"%s\"", format_output(output_values.interruptstatus));
      }
      else{
        printf("%s", format_output(output_values.interruptstatus));
      }
  }
  if (flags.interruptcapture == 1){
       if (flags.read == 1 || flags.interruptstatus == 1){
        printf(",\"interruptcapture\":\"%s\"", format_output(output_values.interruptcapture));
      }
      else{
        printf("%s", format_output(output_values.interruptcapture));
      }
  }
  printf("\n");
}

char* format_output(char value){
  char *str = malloc(11);
  int z;
  switch (output_format){
    case 1:  // hex
      sprintf(str,"0x%x",value);
      return str;    
    case 2:  // binary      
      strcat(str, "0b");
      for (z = 128; z > 0; z >>= 1)
      {
          strcat(str, ((value & z) == z) ? "1" : "0");
      }
      return str;
    default:  // decimal
      sprintf(str,"%d",value);
      return str;
  }
}