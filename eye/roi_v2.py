import os

import cv2

import gabor

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
  corner_right = (facial_landmarks.part(eye_points[4]).x,
                  facial_landmarks.part(eye_points[4]).y)

  Midpoint_left = midpoint(facial_landmarks.part(eye_points[0]),
                          facial_landmarks.part(eye_points[5]))
  Midpoint_right = midpoint(facial_landmarks.part(eye_points[4]),
                          facial_landmarks.part(eye_points[8]))

  center_top = midpoint(facial_landmarks.part(eye_points[0]),
                        facial_landmarks.part(eye_points[4]))
  center_bottom = midpoint(facial_landmarks.part(eye_points[5]),
                           facial_landmarks.part(eye_points[8]))

  # calculating distance
  horizontal_length = euclidean_distance(Midpoint_left, Midpoint_right)
  vertical_length = euclidean_distance(center_top, center_bottom)

  ratio = horizontal_length / vertical_length

  return ratio

# Changed definition to include only one path, rather than paths for eye, eyebrow etc
def rect1(predictor,i,shotname,picturepath,imgPath ,GaborPath,SheetPath,FeaturesPath, shapeArray, borders, img, dets):

    # Function for ROI detection
 #print(imgPath)

 # create a file PATH to store Eye Path picture
 # Rather than a specific path, we are going to choose what path to pass in
    # So then the path will be general
 if not os.path.exists(imgPath):
    os.mkdir(os.path.join(imgPath))
 cur_dir =os.path.join(imgPath, shotname)
 if not os.path.exists(cur_dir):
     os.mkdir(os.path.join(cur_dir))

 #print('inside the eye')

 BLINK_RATIO_THRESHOLD = 0.6
    # these landmarks are based on the image above
 left_eye_landmarks = [17,18,19,20,21, 36,37,38, 39, 40, 41]
 right_eye_landmarks = [22,23,24,25,26,27,42, 43, 44, 45, 46, 47]

 x = [0]
 y = [0]


 for k, d in enumerate(dets):
     # Go through and calculate right eye (on person)
     # print (k,d)
     shape = predictor(img, d)

     # pass in and use new shapepoints array
     #print('using shape points ', shapeArray)

     leftpoint = shape.part(shapeArray[0]).x
     rightpoint = shape.part(shapeArray[1]).x
     toppoint = shape.part(shapeArray[2]).y
     buttompoint = shape.part(shapeArray[3]).y

     ROIval= img[toppoint+borders[0]:buttompoint+borders[1], leftpoint+borders[2]:rightpoint+borders[3]]
     ROIpath = cur_dir + '/' + str('%02d' % i) + '.jpg'
     cv2.imwrite(ROIpath, ROIval)

     count = 1
     total = 0

     # landmarks = predictor(img, d)
     # Calculating blink ratio for one eye-----
     left_eye_ratio = get_blink_ratio(left_eye_landmarks, shape)
     right_eye_ratio = get_blink_ratio(right_eye_landmarks, shape)
     blink_ratio = (left_eye_ratio + right_eye_ratio) / 2
     # blink_path = cur_dir + '/' + str('%02d' % i) + '.jpg'
     # cv2.imwrite(blink_path, img)
     # x.append(str('%02d' % i))
     if blink_ratio >= BLINK_RATIO_THRESHOLD:
         count += 1
         x.append(1)
         #print(blink_ratio, "unblink")
     elif blink_ratio >= BLINK_RATIO_THRESHOLD and left_eye_ratio < BLINK_RATIO_THRESHOLD:
         print(left_eye_ratio, "Right eye wink")
         total += 1

     elif blink_ratio >= BLINK_RATIO_THRESHOLD and left_eye_ratio < BLINK_RATIO_THRESHOLD:
         print(left_eye_ratio, "Left eye wink")
         total += 1

     else:
         if blink_ratio < BLINK_RATIO_THRESHOLD:
             print(blink_ratio, "blink count here")
             total += 1
             y.append(0)

         count = 1



     # Extract gabor features of right eye
     gabor.Gabor_h(i, ROIpath,imgPath, shotname,GaborPath,SheetPath,FeaturesPath)
     return(i,blink_ratio,left_eye_ratio,right_eye_ratio)