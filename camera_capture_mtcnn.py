#imports
import cv2
from mtcnn_cv2 import MTCNN
from scipy.spatial import distance
import numpy as np
from keras.models import load_model
import itertools

#from PIL import ImageFont, ImageDraw, Image
#fontpath = "/Times New Roman Bold.ttc"

pazak = {0:'Patzak detected!',1:'Chatlanin detected!'}
keypoint_names = ["left_eye", "right_eye", "nose","mouth_left","mouth_right"]
features = [a+'-'+b for (a,b) in list(itertools.permutations(keypoint_names,2))]

def E_distance(u,v):
    #Euclidean distance between 2 vectors
    return distance.euclidean(u,v)

def normXY(XY,x_min,y_min,width,height):
    #XY is a set of (x,y)
    return ((XY[0]-x_min)/(width),(XY[1]-y_min)/(height))

# load the saved model
model = load_model('best_model1.h5')
detector = MTCNN()
video = cv2.VideoCapture(0)

if (video.isOpened() == False):
    print("Web Camera not detected")
while (True):
    ret, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if ret == True:
        location = detector.detect_faces(frame)
        if len(location) > 0:
            for face in location:
                x, y, width, height = face['box']
                x2, y2 = x + width, y + height
                cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 4)

                keypoints = face['keypoints']

                cv2.circle(frame, (keypoints['left_eye']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['right_eye']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['nose']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
                cv2.circle(frame, (keypoints['mouth_right']), 2, (0, 155, 255), 2)

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

                # text
                text = pazak[classPredicted.item(0)]
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                fontScale = 1
                color = (0, 0, 255)
                thickness = 2

                frame = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False)

                """
                font = ImageFont.truetype(fontpath, 32)
                img_pil = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                draw.text((50, 80), "Привет", font=font, fill=(b, g, r, a))
                frame = np.array(img_pil)
                """

        cv2.imshow("Output",frame)
        if cv2.waitKey(1) & 0xFF == 27:#ord('q'):
            break
    else:
        break

video.release()
cv2.destroyAllWindows()
