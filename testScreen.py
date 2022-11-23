from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
#from luma.core import lib

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import sys
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#GPIO define
RST_PIN  = 25 #Reset
CS_PIN   = 8
DC_PIN   = 24
JS_U_PIN = 6  #Joystick Up
JS_D_PIN = 19 #Joystick Down
JS_L_PIN = 5  #Joystick Left
JS_R_PIN = 26 #Joystick Right
JS_P_PIN = 13 #Joystick Pressed
BTN1_PIN = 21
BTN2_PIN = 20
BTN3_PIN = 16

# Some constants
SCREEN_LINES = 4
SCREEN_SAVER = 20.0
CHAR_WIDTH = 19
font = ImageFont.load_default()
width = 128
height = 64
x0 = 0
x1 = 84
y0 = -2
y1 = 12
x2 = x1+7
x3 = x1+14
x4 = x1+9
x5 = x2+9
x6 = x3+9

# init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #Disable warnings
GPIO.setup(JS_U_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_L_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_R_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_P_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# Initialize the display...
serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = DC_PIN, gpio_RST = RST_PIN)
device = sh1106(serial, rotate=2) #sh1106
draw = ImageDraw.Draw(Image.new('1', (width, height)))
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Turn Off the display:
# GPIO.output(RST_PIN,GPIO.LOW)

def click_b1(channel):
    print('b1 clicked')

def click_b2(channel):
    print('b2 clicked')

def click_b3(channel):
    print('b3 clicked')

def joyL(channel):
    print('Joystick = Left')

def joyR(channel):
    print('Joystick = Right')

def joyU(channel):
    print('Joystick = Up')

def joyD(channel):
    print('Joystick = Down')

def joyP(channel):
    print('Joystick Select')
    GPIO.output(RST_PIN,GPIO.LOW)

def draw_scn():
    with canvas(device) as draw:
        LINE0 = "Pazak-Chatlanin Detector Tool"
        LINE1 = "Loading"
        LINE2 = "Initializing"
        LINE3 = "Getting ready"
        
        
        if len(LINE0) > CHAR_WIDTH:
            draw.text((x0, 0),   LINE0[:CHAR_WIDTH], font=font, fill=255)
        else:
            draw.text((x0, 0),   LINE0, font=font, fill=255)
        
        if len(LINE1) > CHAR_WIDTH:
            draw.text((x0, y1),   LINE1[:CHAR_WIDTH], font=font, fill=255)
        else:
            draw.text((x0, y1),   LINE1, font=font, fill=255)

        if len(LINE2) > CHAR_WIDTH:
            draw.text((x0, y1*2), LINE2[:CHAR_WIDTH], font=font, fill=255)
        else:
            draw.text((x0, y1*2), LINE2, font=font, fill=255)

        if len(LINE3) > CHAR_WIDTH:
            draw.text((x0, y1*3), LINE3[:CHAR_WIDTH], font=font, fill=255)
        else:
            draw.text((x0, y1*3), LINE3, font=font, fill=255)


GPIO.add_event_detect(BTN1_PIN, GPIO.RISING, callback=click_b1, bouncetime=200)
GPIO.add_event_detect(BTN2_PIN, GPIO.RISING, callback=click_b2, bouncetime=200)
GPIO.add_event_detect(BTN3_PIN, GPIO.RISING, callback=click_b3, bouncetime=200)
GPIO.add_event_detect(JS_L_PIN, GPIO.RISING, callback=joyL, bouncetime=200)
GPIO.add_event_detect(JS_R_PIN, GPIO.RISING, callback=joyR, bouncetime=200)
GPIO.add_event_detect(JS_U_PIN, GPIO.RISING, callback=joyU, bouncetime=200)
GPIO.add_event_detect(JS_D_PIN, GPIO.RISING, callback=joyD, bouncetime=200)
GPIO.add_event_detect(JS_P_PIN, GPIO.RISING, callback=joyP, bouncetime=200)

# Main Loop
try:
    while True:
        draw_scn()
    #time.sleep(1)

except:
    print("Stopped", sys.exc_info()[0])
    raise
GPIO.cleanup()