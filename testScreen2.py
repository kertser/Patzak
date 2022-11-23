#!/usr/bin/python
# -*- coding:utf-8 -*-

import SH1106
import time
import config
#import traceback

from PIL import Image,ImageDraw,ImageFont
    
def printText(firstLine,x1y1, secondLine,x2y2):
    # Create blank image for drawing.
    x1,y1 = x1y1
    x2,y2 = x2y2
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

try:
    disp = SH1106.SH1106()

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    printText('Обнаружен',(25,0),'Пацак!',(28,20))
    time.sleep(2)
    printText('Обнаружен',(25,0),'Чатланин!',(15,20))
    time.sleep(2)
    disp.reset()
    disp.clear()    

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    #epdconfig.module_exit()
    exit()
