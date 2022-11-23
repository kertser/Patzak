# Config and keybindings for the script:

import RPi.GPIO as GPIO
import time
from smbus2 import SMBus
import spidev

#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24
BL_PIN          = 18

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

Device_SPI = 1
Device_I2C = 0

if(Device_SPI == 1):
    Device = Device_SPI
    spi = spidev.SpiDev(0, 0)
else :
    Device = Device_I2C
    address         = 0x3C
    bus = SMBus(1)

def initKeys():
    #init GPIO
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
    GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
    GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
    GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
    GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
    GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

def digital_write(pin, value):
    GPIO.output(pin, value)

def digital_read(pin):
    #return GPIO.input(BUSY_PIN)
    return GPIO.input(pin)

def delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)

def spi_writebyte(data):
    # SPI.writebytes(data)
    spi.writebytes([data[0]])

def i2c_writebyte(reg, value):
    bus.write_byte_data(address, reg, value)
    
    # time.sleep(0.01)
def module_init():
    # print("module_init")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(DC_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(BL_PIN, GPIO.OUT)

    
    # SPI.max_speed_hz = 2000000
    # SPI.mode = 0b00
    # i2c_writebyte(0xff,0xff)
    if(Device == Device_SPI):
        # spi.SYSFS_software_spi_begin()
        # spi.SYSFS_software_spi_setDataMode(0);
        # spi.SYSFS_software_spi_setClockDivider(1);
        spi.max_speed_hz = 10000000
        spi.mode = 0b00
    
    GPIO.output(CS_PIN, 0)
    GPIO.output(BL_PIN, 1)
    GPIO.output(DC_PIN, 0)
    return 0

def keybindings():
    
    keybinding = ""
    # with canvas(device) as draw:
    if GPIO.input(KEY_UP_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "Up" 
        
    if GPIO.input(KEY_LEFT_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "left"
        
    if GPIO.input(KEY_RIGHT_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "right"
        
    if GPIO.input(KEY_DOWN_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "down"

    if GPIO.input(KEY_PRESS_PIN): # button is released
        pass
    else: # button is pressed:
       keybinding = "center"
        
    if GPIO.input(KEY1_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "KEY1"
        
    if GPIO.input(KEY2_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "KEY2"
        
    if GPIO.input(KEY3_PIN): # button is released
        pass
    else: # button is pressed:
        keybinding = "KEY3"
    
    return keybinding

def module_exit():
    GPIO.output(RST_PIN, 0)
    GPIO.output(DC_PIN, 0)
    GPIO.cleanup()
