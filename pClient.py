# Testing the remote client-server setup
import requests
import cv2

width = 320
height = 200
dim = (width, height)

img_name = "face.jpg"
cam = cv2.VideoCapture(0,cv2.CAP_V4L2)
url = 'http://192.168.1.100:8000/upload'
try:
    ret, frame = cam.read()
    img = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    #img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(img_name, img)
    file = {'file': open(img_name, 'rb')}
    resp = requests.post(url=url, files=file)
    print(resp.json())
    cam.release()
except requests.ConnectionError as exceptConnect:
    # print(exceptConnect)
    print('Server Refused Connection')