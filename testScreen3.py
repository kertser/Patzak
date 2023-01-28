#!/usr/bin/python
# -*- coding:utf-8 -*-

import SH1106
import config #and all that is there
import time

import subprocess

from PIL import Image,ImageDraw,ImageFont
    
def printText(firstLine,secondLine):
    # Create blank image for drawing.
    x1 = 120/2-(len(firstLine)/2)*8
    y1 = 0
    x2 = 120/2-(len(secondLine)/2)*10
    y2 = 20
    
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('Font.ttf', 20)
    font10 = ImageFont.truetype('Font.ttf',13)
    
    draw.line([(0,0),(127,0)], fill = 0)
    draw.line([(0,0),(0,63)], fill = 0)
    draw.line([(0,63),(127,63)], fill = 0)
    draw.line([(127,0),(127,63)], fill = 0)
    
    draw.text((x1,y1), firstLine, font = font10, fill = 0)
    draw.text((x2,y2), secondLine, font = font, fill = 0)

    disp.ShowImage(disp.getbuffer(image1))    

try: #init
    # 240x240 display with hardware SPI:
    disp = SH1106.SH1106()
    config.initKeys()

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    printText('Обнаружен','Пацак!')
    time.sleep(2)
    printText('Обнаружен','Чатланин!')
    time.sleep(2)
    #disp.reset()
    #disp.clear()
    
    while True:
        status = config.keybindings()
        if status == "KEY2":
            config.module_exit()
            exit()

except IOError as e:
    print(e)
    
