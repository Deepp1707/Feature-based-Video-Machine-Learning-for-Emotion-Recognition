import numpy as np
import cv2
import os
import glob
from PIL import Image
import scipy.ndimage as ndi
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from skimage import io,measure,color,data,filters
import gabor
import dlib
import math


# Getting to know blink ratio

def midpoint(point1, point2):
 return (point1.x + point2.x) / 2, (point1.y + point2.y) / 2


def euclidean_distance(point1, point2):
 return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_blink_ratio(eye_points, facial_landmarks):
  # loading all the required points
  corner_left = (facial_landmarks.part(eye_points[0]).x,
                 facial_landmarks.part(eye_points[0]).y)
  corner_right = (facial_landmarks.part(eye_points[3]).x,
                  facial_landmarks.part(eye_points[3]).y)

  center_top = midpoint(facial_landmarks.part(eye_points[1]),
                        facial_landmarks.part(eye_points[2]))
  center_bottom = midpoint(facial_landmarks.part(eye_points[5]),
                           facial_landmarks.part(eye_points[4]))

  # calculating distance
  horizontal_length = euclidean_distance(corner_left, corner_right)
  vertical_length = euclidean_distance(center_top, center_bottom)

  ratio = horizontal_length / vertical_length

  return ratio


def rect5(detector,predictor,i,shotname,picturepath,EyePath,R_EyeBrowPath,R_EyePath,GaborPath,SheetPath,FeaturesPath,eye_blink):


 img = cv2.imread(picturepath)
 dets = detector(img, 1)

 if not os.path.exists(eye_blink):
    os.mkdir(os.path.join(eye_blink))
 cur_dir =os.path.join(eye_blink, shotname)
 if not os.path.exists(cur_dir):
     os.mkdir(os.path.join(cur_dir))
 BLINK_RATIO_THRESHOLD = 5.7

 # these landmarks are based on the image above
 left_eye_landmarks = [36, 37, 38, 39, 40, 41]
 right_eye_landmarks = [42, 43, 44, 45, 46, 47]

 x = [0]
 y = [0]

 # Detecting Eyes using landmarks in dlib-----
 for k, d in enumerate(dets):

     count = 1
     total = 0

     landmarks = predictor(img, d)
     # Calculating blink ratio for one eye-----
     left_eye_ratio = get_blink_ratio(left_eye_landmarks, landmarks)
     right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
     blink_ratio = (left_eye_ratio + right_eye_ratio) / 2
     blink_path = cur_dir + '/' + str('%02d' % i) + '.jpg'
     cv2.imwrite(blink_path, img)
     #x.append(str('%02d' % i))
     if blink_ratio > BLINK_RATIO_THRESHOLD:
         print(blink_ratio, "Blink counts here")
         count += 1
         #y.append(blink_ratio)
     else:
      if count <= BLINK_RATIO_THRESHOLD:
          print(blink_ratio, "Unblink")
          total += 1
          #y.append(blink_ratio)

          count = 1
      else:
          if count is None:
              break



 x.append(str('%02d' % i))
 y.append(blink_ratio)
 print(x)
 print(y)

 #plt.plot(x,y)
 #plt.show()


   #shape = predictor(img, d)
  #for face in faces:









    #blink_path = cur_dir + '/' + str('%02d' % i) + '.jpg'
    #cv2.imwrite(blink_path, img)




    # Blink detected! Do Something!
    #cv2.putText(img, "Blink Count: {}".format(total), (5, 50), cv2.FONT_HERSHEY_SIMPLEX,
                #1, (255, 255, 255), 1, cv2.LINE_AA)

  #cv2.imshow('BlinkDetector', frame)
  #key = cv2.waitKey(1)
  #if key == 27:
   #break

  # blink_graph = numpy.arange(0,5,2.5)
 # releasing the VideoCapture object
 #cap.release()
 # print(BLINK_RATIO_THRESHOLD)
 # eye_blink_signal = []
 # eye_blink_signal.append(blink_ratio)
 # plt.plot(eye_blink_signal)
 # plt.show()
 #cv2.destroyAllWindows()