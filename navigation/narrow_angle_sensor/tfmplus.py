#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 # Package:   tfmplus
 # Inception: 10 MAR 2021
 # Described: Python package for the Benewake TFMini-Plus Lidar sensor
 #            The TFMini-Plus is a unique product. TFMini-Plus
 #            packages are not compatible with the TFMini.
 # Developer: Bud Ryerson
 # v0.0.18 - 21 MAY 2021
 # v0.1.0  - 06 SEP 2021 - Corrected (reversed) Enable/Disable commands.
             Changed three command names
               OBTAIN_FIRMWARE_VERSION is now GET_FIRMWARE_VERSION
               RESTORE_FACTORY_SETTINGS is now HARD_RESET
               SYSTEM_RESET is now SOFT_RESET
 #
 # Default settings for the TFMini-Plus are a 115200 serial baud rate
 # and a 100Hz measurement frame rate. The device will begin returning
 # measurement data immediately on power up.
 #
 # 'begin( port, rate)' passes a string of the name of the
 #  host serial port and a baud rate to the module.
 #  Returns boolean value whether serial data is available.
 #  Also sets a public one byte status code, defined below.
 #
 # `getData()` receives a frame of data from the device and
 #  sets the values of three variables:
 #  • `dist` = distance in centimeters,
 #  • `flux` = signal strength in arbitrary units, and
 #  • `temp` = degrees centigrade as a coded number
 #  Returns a boolean value whether completed without error.
 #  Also sets a one byte `status` code.
 #
 # `sendCommand( cmnd, param)` sends appropriate command
 #  and parameter values, returns a boolean success value
 #  and sets an explanatory, public, one byte `status` code.
 #  Commands are chosen from the module's defined commands.
 #  Parameter values can be entered directly (115200, 250, etc)
 #  but for safety, should be chosen from the module's
 #  defined values. Incorrect values can render the device
 #  permanently uncommunicative.
 #
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'''

import time
import serial

status = 0           # error status code
dist =   0           # distance to target
flux =   0           # signal quality or intensity
temp =   0           # internal chip temperature
version = bytearray( 3)   # firmware version number

# Buffer sizes
TFMP_FRAME_SIZE =  9   # Size of one data frame = 9 bytes
TFMP_COMMAND_MAX = 8   # Longest command = 8 bytes
TFMP_REPLY_SIZE =  8   # Longest command reply = 8 bytes
# Buffers
frame = bytearray( TFMP_FRAME_SIZE)   # firmware version number
reply = bytearray( TFMP_REPLY_SIZE)   # firmware version number

# Timeout Limits for various functions
TFMP_MAX_READS          = 20   # readData() sets SERIAL error
MAX_BYTES_BEFORE_HEADER = 20   # getData() sets HEADER error
MAX_ATTEMPTS_TO_MEASURE = 20

TFMP_DEFAULT_ADDRESS    = 0x10  # default I2C slave address
                                # as hexidecimal integer
#
# System Error Status Condition
TFMP_READY        =  0  # no error
TFMP_SERIAL       =  1  # serial timeout
TFMP_HEADER       =  2  # no header found
TFMP_CHECKSUM     =  3  # checksum doesn't match
TFMP_TIMEOUT      =  4  # I2C timeout
TFMP_PASS         =  5  # reply from some system commands
TFMP_FAIL         =  6  #           "
TFMP_I2CREAD      =  7
TFMP_I2CWRITE     =  8
TFMP_I2CLENGTH    =  9
TFMP_WEAK         = 10  # Signal Strength ≤ 100
TFMP_STRONG       = 11  # Signal Strength saturation
TFMP_FLOOD        = 12  # Ambient Light saturation
TFMP_MEASURE      = 13

#  Return TRUE/FALSE whether receiving serial data from
#  device, and set system status to provide more information.
def begin( port, rate):
    ''' Set serial port and test for data'''
    global pStream
    pStream = serial.Serial( port, rate)
    time.sleep(0.2)             #  Give port 200ms to initalize
    if pStream.inWaiting() > 0:    #  If data present...
        status = TFMP_READY     #  return status as READY
        return True
    else:                       #  Otherwise...
        status = TFMP_SERIAL    #  return status as SERIAL ERROR
        return False

''' - - - - - -  TFMini Plus data formats  - - - - - - - - -
  Data Frame format:
  Byte0  Byte1  Byte2   Byte3   Byte4   Byte5   Byte6   Byte7   Byte8
  0x59   0x59   Dist_L  Dist_H  Flux_L  Flux_H  Temp_L  Temp_H  CheckSum_
  Data Frame Header character: Hex 0x59, Decimal 89, or "Y"

  Command format:
  Byte0  Byte1   Byte2   Byte3 to Len-2  Byte Len-1
  0x5A   Length  Cmd ID  Payload if any   Checksum
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''

#  Return TRUE/FALSE whether data received without error
#  and set system status to provide more information.
def getData():
    ''' Get serial frame data from device'''
    
    # make data variables global
    global status, dist, flux, temp

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 1 - Get data from the device.
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Set 1 second timeout if HEADER code never appears
    #  or serial data never becomes available.
    serialTimeout = time.time() + 1000
    #  Flush all but last frame of data from the serial buffer.
    while( pStream.inWaiting() > TFMP_FRAME_SIZE):
        pStream.read()
    #  Read one byte from the serial buffer into the data buffer's
    #  'plus one' position, then left shift the whole array 1 byte
    #  and repeat until the two HEADER bytes show up as the first
    #  two bytes in the array.
    frame = bytearray( TFMP_FRAME_SIZE)   #  'frame' data buffer
    while( frame[ 0] != 0x59) or ( frame[ 1] != 0x59):
        if pStream.inWaiting():
            #  Read 1 byte into the 'frame' plus one position.
            frame.append( pStream.read()[0])
            #  Shift entire length of 'frame' one byte left.
            frame = frame[ 1:]
        #  If no HEADER or serial data not available
        #  after more than one second...
        if time.time() >  serialTimeout:
            status = TFMP_HEADER   #  ...then set error
            return False

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 2 - Perform a checksum test.
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Clear the 'chkSum' variable declared in 'TFMPlus.h'
    chkSum = 0
    #  Add together all bytes but the last.
    for i in range( TFMP_FRAME_SIZE -1):
        chkSum += frame[ i]
    #   If the low order byte does not equal the last byte...
    if( ( chkSum & 0xFF) != frame[ TFMP_FRAME_SIZE -1]):
        status = TFMP_CHECKSUM  #  ...then set error
        return False

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 3 - Interpret the frame data
    #           and if okay, then go home
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    dist = (frame[3] * 256) + frame[2]
    flux = (frame[5] * 256) + frame[4]
    temp = (frame[7] * 256) + frame[6]
    #  Convert temp code to degrees Celsius.
    temp = ( temp >> 3) - 256
    #  Convert Celsius to degrees Farenheit
    #  temp = ( temp * 9 / 5) + 32

    #  - - Evaluate Abnormal Data Values - -
    #  Values are from the TFMini-S Product Manual
    #  Signal strength <= 100
    if( dist == -1):     status = TFMP_WEAK
    #  Signal Strength saturation
    elif( flux == -1):   status = TFMP_STRONG
    #  Ambient Light saturation
    elif( dist == -4):   status = TFMP_FLOOD
    #  Data is apparently okay
    else:                status = TFMP_READY

    if( status != TFMP_READY):
        return False;
    else:
        return True;


#  = = = = =  SEND A COMMAND TO THE DEVICE  = = = = = = = = = =0
#
#  - - -  Command Codes - - - - -
#  The 'sendCommand()' function expects the command
#  (cmnd) code to be in the the following format:
#  0x     00       00       00       00
#      one byte  command  command   reply
#      payload   number   length    length
GET_FIRMWARE_VERSION      = 0x00010407   # returns 3 byte firmware version
TRIGGER_DETECTION         = 0x00040400   # frame rate must be set to zero
                                         # returns a 9 byte data frame
SOFT_RESET                = 0x00020405   # returns a 1 byte pass/fail (0/1)
HARD_RESET                = 0x00100405   #           "
SAVE_SETTINGS             = 0x00110405   # This must follow every command
                                         # that modifies volatile parameters.
                                         # Returns a 1 byte pass/fail (0/1)

SET_FRAME_RATE            = 0x00030606   # Each of these commands return
SET_BAUD_RATE             = 0x00060808   # an echo of the command
STANDARD_FORMAT_CM        = 0x01050505   #           "
PIXHAWK_FORMAT            = 0x02050505   #           "
STANDARD_FORMAT_MM        = 0x06050505   #           "
ENABLE_OUTPUT             = 0x01070505   #           "
DISABLE_OUTPUT            = 0x00070505   #           "
SET_I2C_ADDRESS           = 0x100B0505   #           "

SET_SERIAL_MODE           = 0x000A0500   # default is Serial (UART)
SET_I2C_MODE              = 0x010A0500   # set device as I2C slave

I2C_FORMAT_CM             = 0x01000500   # returns a 9 byte data frame
I2C_FORMAT_MM             = 0x06000500   #           "
#
# - - Command Parameters - - - - 
BAUD_9600          = 0x002580   # UART serial baud rate
BAUD_14400         = 0x003840   # expressed in hexidecimal
BAUD_19200         = 0x004B00
BAUD_56000         = 0x00DAC0
BAUD_115200        = 0x01C200
BAUD_460800        = 0x070800
BAUD_921600        = 0x0E1000

FRAME_0            = 0x0000    # internal measurement rate
FRAME_1            = 0x0001    # expressed in hexidecimal
FRAME_2            = 0x0002
FRAME_5            = 0x0005    # set to 0x0003 in prior version
FRAME_10           = 0x000A
FRAME_20           = 0x0014
FRAME_25           = 0x0019
FRAME_50           = 0x0032
FRAME_100          = 0x0064
FRAME_125          = 0x007D
FRAME_200          = 0x00C8
FRAME_250          = 0x00FA
FRAME_500          = 0x01F4
FRAME_1000         = 0x03E8
#
#  Create a proper command byte array, send the command,
#  get a repsonse, and return the status
def sendCommand( cmnd, param):
    ''' Send serial command and get reply data'''

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 1 - Build the command data to send to the device
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # From 32bit 'cmnd' integer, create a four byte array of:
    # reply length, command length, command number and a one byte parameter
    cmndData = bytearray( cmnd.to_bytes( TFMP_COMMAND_MAX, byteorder = 'little'))

    replyLen = cmndData[ 0]        #  Save the first byte as reply length.
    cmndLen = cmndData[ 1]         #  Save the second byte as command length.
    cmndData[ 0] = 0x5A            #  Set the first byte to HEADER code.

    if( cmnd == SET_FRAME_RATE):                                     #  If the command is Set FrameRate...
        cmndData[3:2] = param.to_bytes( 2, byteorder = 'little')     #  add the 2 byte FrameRate parameter.
    elif( cmnd == SET_BAUD_RATE):                                    #  If the command is Set BaudRate...
        cmndData[3:3] = param.to_bytes( 3, byteorder = 'little')     #  add the 3 byte BaudRate parameter.

    cmndData = cmndData[0:cmndLen]  # re-establish command data length
    
    #  Create a checksum byte for the command data array.
    chkSum = 0
    #  Add together all bytes but the last.
    for i in range( cmndLen -1):
        chkSum += cmndData[ i]
    #  and save it as the last byte of command data.
    cmndData[ cmndLen -1] = ( chkSum & 0xFF)
    
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 2 - Send the command data array to the device
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    pStream.reset_input_buffer()    #  flush input buffer
    pStream.reset_output_buffer()   #  flush output buffer
    pStream.write( cmndData)        #  send command data
        
    #  + + + + + + + + + + + + + + + + + + + + + + + + +
    #  If the command does not expect a reply, then we're
    #  finished here. Go home.
    if( replyLen == 0):
        return True
    #  + + + + + + + + + + + + + + + + + + + + + + + + +

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 3 - Get command reply data back from the device.
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Set a one second timer to timeout if HEADER never appears
    #  or serial data never becomes available
    serialTimeout = time.time() + 1000
    #  Establish 'reply' bytearray and fill with zeros
    reply = bytearray( replyLen)
    
    #  1) Read one byte from serial buffer
    #  2) Append byte to end of 'reply'
    #  3) Left shift entire array by one byte.
    #  4) Repeat until 'HEADER' and 'replyLen'
    #     appear as first two bytes in array.
    while( reply[ 0] != 0x5A) or (reply[ 1] != replyLen):
        if( pStream.inWaiting()):
            #  Read 1 byte into the 'frame' plus one position.
            reply.append( pStream.read()[0])
            #  Shift entire length of 'frame' one byte left.
            reply = reply[ 1:]
        #  If HEADER/replyLen combo does do not
        #  appear after more than one second...
        if( time.time() >  serialTimeout):
            status = TFMP_HEADER   #  ...then set error type
            return False           # and return 'False'.

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 4 - Perform a checksum test.
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Clear the 'chkSum' variable declared in 'TFMPlus.h'
    chkSum = 0
    #  Add together all bytes but the last.
    for i in range( replyLen -1):
        chkSum += reply[ i]
    #  If the low order byte does not equal the last byte...
    if( ( chkSum & 0xFF) != reply[ replyLen - 1]):
      status = TFMP_CHECKSUM  #  ...then set error
      return False            #  and return 'False.'

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 5 - Interpret different command responses.
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if( cmnd == GET_FIRMWARE_VERSION):
        version[ 0] = reply[ 5]  #  set firmware version.
        version[ 1] = reply[ 4]
        version[ 2] = reply[ 3]
    else:
        if( cmnd == SOFT_RESET or
            cmnd == HARD_RESET or
            cmnd == SAVE_SETTINGS ):
            if( reply[ 3] == 1):    #  If PASS/FAIL byte non-zero...
                status = TFMP_FAIL  #  then set status to 'FAIL'...
                return False        #  and return 'False'.

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #  Step 6 - Set status to 'READY' and return 'True'
    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    status = TFMP_READY
    return True

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  - - - - -    The following are for testing purposes   - - - -
#     They interpret error status codes and display HEX data
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#  Called by either 'printFrame()' or 'printReply()'
#  Print status condition either 'READY' or error type
# dumb (JDCC) ... to python 2.7
# remove the no linebreaks
def printStatus():
    ''' Print status condition'''
    print("Status: ")
    if( status == TFMP_READY):       print( "READY")
    elif( status == TFMP_SERIAL):    print( "SERIAL")
    elif( status == TFMP_HEADER):    print( "HEADER")
    elif( status == TFMP_CHECKSUM):  print( "CHECKSUM")
    elif( status == TFMP_TIMEOUT):   print( "TIMEOUT")
    elif( status == TFMP_PASS):      print( "PASS")
    elif( status == TFMP_FAIL):      print( "FAIL")
    elif( status == TFMP_I2CREAD):   print( "I2C-READ")
    elif( status == TFMP_I2CWRITE):  print( "I2C-WRITE")
    elif( status == TFMP_I2CLENGTH): print( "I2C-LENGTH")
    elif( status == TFMP_WEAK):      print( "Signal weak")
    elif( status == TFMP_STRONG):    print( "Signal saturation")
    elif( status == TFMP_FLOOD):     print( "Ambient light saturation")
    else:                            print( "OTHER")
    print()
#
#  Print error type and HEX values
#  of each byte in the data frame
def printFrame():
    '''Print status and frame data'''
    printStatus();
    print("Data:")  # no carriage return
    for i in range( TFMP_FRAME_SIZE):
        #  >>> f"{value:#0{padding}X}"
        # Pad hex number with 0s to length of n characters
        print(f" {frame[ i]:0{2}X}")
    print()
#   
#  Print error type and HEX values of
#  each byte in the command response frame.
def printReply():
    '''Print status and reply data'''
    printStatus()
    #  Print the Hex value of each byte
    for i in range( TFMP_REPLY_SIZE):
        print(f" {reply[ i]:0{2}X}")    
    print()

#  Definitions that need to be exported
__all__ = ['GET_FIRMWARE_VERSION', 'TRIGGER_DETECTION', 'SOFT_RESET',
           'HARD_RESET', 'SAVE_SETTINGS', 'SET_FRAME_RATE',
           'SET_BAUD_RATE', 'STANDARD_FORMAT_CM', 'PIXHAWK_FORMAT',
           'STANDARD_FORMAT_MM', 'ENABLE_OUTPUT', 'DISABLE_OUTPUT',
           'SET_I2C_ADDRESS', 'SET_SERIAL_MODE', 'SET_I2C_MODE',
           'I2C_FORMAT_CM', 'I2C_FORMAT_MM',
           'BAUD_9600', 'BAUD_14400', 'BAUD_19200', 'BAUD_56000',
           'BAUD_115200', 'BAUD_460800', 'BAUD_921600',
           'FRAME_0', 'FRAME_1', 'FRAME_2', 'FRAME_5', 'FRAME_10',
           'FRAME_20', 'FRAME_25', 'FRAME_50', 'FRAME_100', 'FRAME_125',
           'FRAME_200', 'FRAME_250', 'FRAME_500', 'FRAME_1000']


# ====   For troubleshooting: This code  ====
# ====   formats a value as hexidecimal  ====
'''
for i in range( len(cmndData)):
    print( f" {cmndData[i]:0{2}X}", end='')
print()
'''
# f"{value:#0{padding}X}"
# formats 'value' as a hex number padded with
# 0s to the length of 'padding'
#============================================

# If this module is executed by itself
if __name__ == "__main__":
    print( "tfmplus - This Python module supports" +\
           " the Benewake TFMini-Plus Lidar device")
