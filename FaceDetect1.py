# General Imports
import urllib.request
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import tensorflow as tf

from matplotlib.patches import Rectangle

from numpy import asarray
from PIL import Image

# Kill the regular warnings and tensorFlow warnings:
import warnings
warnings.filterwarnings(action='ignore')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Store image from internet as local image
def store_image(url, local_file_name):
    with urllib.request.urlopen(url) as resource:
        with open(local_file_name, 'wb') as f:
            f.write(resource.read())

image = plt.imread('iacocca_1.jpg')

"""
For every face, a Python dictionary is returned, which contains three keys. 
The box key contains the boundary of the face within the image. 
It has four values: x- and y-coordinates of the top left vertex, width, and height of the rectangle containing the face. 
The other keys are confidence and keypoints. 
The keypoints key contains a dictionary containing the features of a face that were detected, along with their coordinates
"""

#detector = MTCNN()
#faces = detector.detect_faces(image)

def highlight_faces(image_path, faces):
  # display image
  image = plt.imread(image_path)
  plt.imshow(image)

  ax = plt.gca()

  # for each face, draw a rectangle based on coordinates
  for face in faces:
    x, y, width, height = face['box']
    face_border = Rectangle((x, y), width, height,
                          fill=False, color='red')
    ax.add_patch(face_border)
  plt.show()

def extract_face_from_image(image_path, required_size=(224, 224)):
  # load image and detect faces
  image = plt.imread(image_path)
  detector = MTCNN()
  faces = detector.detect_faces(image)

  for face in faces:
      print(face['keypoints'])

  face_images = []

  for face in faces:
    # extract the bounding box from the requested face
    x1, y1, width, height = face['box']
    x2, y2 = x1 + width, y1 + height

    # extract the face
    face_boundary = image[y1:y2, x1:x2]

    # resize pixels to the model size
    face_image = Image.fromarray(face_boundary)
    face_image = face_image.resize(required_size)
    face_array = asarray(face_image)
    face_images.append(face_array)

  return face_images

extracted_face = extract_face_from_image('iacocca_1.jpg')

# Display the first face from the extracted faces
plt.imshow(extracted_face[0])
plt.show()
