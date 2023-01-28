#!/usr/bin/python
# -*- coding:utf-8 -*-

import SH1106
import config #and all that is there
import time
import itertools
from scipy.spatial import distance

import subprocess

from PIL import Image,ImageDraw,ImageFont

stackdetect = [] # stack of the detected values:
maxSize = 3 # max size of this stack (for faster board it can be 20)
countNANS = 0

pazak = {0:'Patzak',1:'Chatlanin'}
keypoint_names = ["left_eye", "right_eye", "nose","mouth_left","mouth_right"]
features = [a+'-'+b for (a,b) in list(itertools.permutations(keypoint_names,2))]

def E_distance(u,v):
    #Euclidean distance between 2 vectors
    return distance.euclidean(u,v)

def normXY(XY,x_min,y_min,width,height):
    #XY is a set of (x,y)
    return ((XY[0]-x_min)/(width),(XY[1]-y_min)/(height))

def printText(firstLine,secondLine):
    # Create blank image for drawing.
    x1 = 125/2-(len(firstLine)/2)*7
    y1 = 0
    x2 = 125/2-(len(secondLine)/2)*10
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

def classifier() -> str:
    ret, frame = video.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if ret == True:
        location = detector.detect_faces(frame)
        if len(location) > 0:
            for face in location:
                x, y, width, height = face['box']
                x2, y2 = x + width, y + height
                #cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 4)

                keypoints = face['keypoints']

                #cv2.circle(frame, (keypoints['left_eye']), 2, (0, 155, 255), 2)
                #cv2.circle(frame, (keypoints['right_eye']), 2, (0, 155, 255), 2)
                #cv2.circle(frame, (keypoints['nose']), 2, (0, 155, 255), 2)
                #cv2.circle(frame, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
                #cv2.circle(frame, (keypoints['mouth_right']), 2, (0, 155, 255), 2)

                # Construct Feature Vector
                x_min, y_min, width, height = face['box']
                featureVector = []
                for feature in features:
                    x1, y1 = normXY((face['keypoints'])[feature.split('-')[0]], x_min, y_min, width,
                                    height)
                    x2, y2 = normXY((face['keypoints'])[feature.split('-')[1]], x_min, y_min, width,
                                    height)
                    featureVector.append(E_distance((x1, y1), (x2, y2)))

                classPredicted = model.predict(np.asarray([featureVector]))
                classPredicted = (classPredicted > 0.5)  # sigmoid
                stackdetect.append(classPredicted.item(0))
                if len(stackdetect) > maxSize:
                    stackdetect.pop(stackdetect[0])
                detected = mean(stackdetect)

                # return the class
                return pazak[int(round(detected,0))]
        else:
            return 'None'

try: #init
    # 240x240 display with hardware SPI:
    disp = SH1106.SH1106()
    config.initKeys()

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    printText('Loading Modules','Please Wait')
    try:
        # get the imported modules, load the classifier and init camera:
        
        #imports
        import cv2
        from mtcnn_cv2 import MTCNN
        import numpy as np
        from keras.models import load_model
        from statistics import mean
        import numpy as np
        
        # load the saved model
        model = load_model('best_model1.h5')
        print('Model Loaded')
        
        # init the camera
        detector = MTCNN()
        video = cv2.VideoCapture(0,cv2.CAP_V4L2)
        
        if (video.isOpened() == False):
            printText('Web Camera','Not Detected')
            time.sleep(2)
            config.module_exit()
            exit()
            
        printText('Modules Loaded','Get Ready')
    except:
        # something got wrong:
        printText('Init Failure','Error loading')
        time.sleep(2)
        config.module_exit()
        exit()
    
    status = config.keybindings()
    while status!="KEY2":
        
        if status == "left": #debug only
            printText('Обнаружен','Пацак!')
        if status == "right": #debug only
            printText('Обнаружен','Чатланин!')
        if status == "center":
            print('detecting')
            printText('Наведите Камеру','Detecting!')
            detectedClass = classifier()
            if detectedClass == 'Patzak':
                printText('Обнаружен','Пацак!')
                #countNANS = 0
            elif detectedClass == 'Chatlanin':
                printText('Обнаружен','Чатланин!')
                #countNANS = 0
            else:
                printText('Наведите Камеру','Не вижу!')
                """
                countNANS += 1
                if countNANS > 20:
                    printText('Наведите Камеру','Не вижу!')
                    countNans = 100
                """
            detectedClass = 'None'
        
        status = config.keybindings()
        
    print('shutting down, please wait')
    video.release()
    disp.reset()
    disp.clear()
    config.module_exit()
    exit()

except IOError as e:
    print(e)
    
