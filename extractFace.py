import matplotlib.pyplot as plt
from scipy.spatial import distance
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN
from PIL import Image
import numpy as np
import pandas as pd
import itertools
from keras.models import load_model
pazak = {0:'Pazak',1:'Chatlanin'}

# load the saved model
model = load_model('best_model1.h5')

def M_distance(u,v):
    iv = [[1, 0.5], [0.5, 1]]
    return distance.mahalanobis(list(u), list(v), iv)

def E_distance(u,v):
    #Euclidean distance between 2 vectors
    return distance.euclidean(u,v)

def normXY(XY,x_min,y_min,width,height):
    #XY is a set of (x,y)
    return ((XY[0]-x_min)/(width),(XY[1]-y_min)/(height))

def extract_face_from_image(image_path, required_size=(240, 240)):
    # load image and detect faces
    image = plt.imread(image_path)
    detector = MTCNN()
    faces = detector.detect_faces(image)

    #This is just a debug print:
    # for face in faces:
    #print(face['keypoints'])
    #print(f"The Mahalanobis distance is :{round(M_distance(face['keypoints']['left_eye'],face['keypoints']['right_eye']),2)}")

    face_images = []

    for face in faces:
        # extract the bounding box from the requested face
        x1, y1, width, height = face['box']
        x2, y2 = x1 + width, y1 + height

        # extract the face
        face_boundary = image[y1:y2, x1:x2]

        face_image = Image.fromarray(face_boundary)

        face_array = np.asarray(face_image)
        face_images.append({'image':face_array,'keypoints':face['keypoints'],'box':face['box']})

    return face_images

#---- predict class:

keypoint_names = ["left_eye", "right_eye", "nose","mouth_left","mouth_right"]
features = [a+'-'+b for (a,b) in list(itertools.permutations(keypoint_names,2))]

df = pd.DataFrame(columns=features)
extracted_face = extract_face_from_image('opencv_frame_0.jpg')
x_min, y_min, width, height = extracted_face[0]['box']

#Construct Feature Vector
featureVector = []
for feature in features:
    x1,y1 = normXY((extracted_face[0]['keypoints'])[feature.split('-')[0]],x_min,y_min,width,height)
    x2,y2 = normXY((extracted_face[0]['keypoints'])[feature.split('-')[1]],x_min,y_min,width,height)
    #df.at[0,feature] = E_distance((x1,y1),(x2,y2))
    featureVector.append(E_distance((x1,y1),(x2,y2)))

model = load_model('best_model1.h5')
#nprint(np.asarray([featureVector]))
classPredicted = model.predict(np.asarray([featureVector]))
classPredicted = (classPredicted>0.5) #sigmoid
print(pazak[classPredicted.item(0)])

def plotImage(extracted_face):
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')
    plt.imshow(extracted_face[0]['image'])

    x1, y1, width, height = extracted_face[0]['box']
    keypoint_values = list(extracted_face[0]['keypoints'].values())
    keypoint_values = [((value[0]-x1),(value[1]-y1)) for value in keypoint_values]

    for xx,yy in keypoint_values:
        circ = Circle((xx,yy),3, color='Red')
        ax.add_patch(circ)

    plt.show()