import glob
import cv2
import os
#import roi
#import r_eye
#import r_eyebrow
#import l_eyebrow
import gabor
#from gabor_l_eb import *
#import features
import frames2
import dlib
#from eye_blinking import *

# Here, we can optimise by defining the folder name here.  Then we can reuse it below.
# Means when we change it, we only need to change it once, not repeatedly
#Dr andrew's file path
#vidFolder = 'C:\Users\User\OneDrive\code\Emotion-recognition'
# Misbah File Path
vidFolder = 'C:/Users/User/OneDrive/code/eyeblink'
#vidFile = 'bbaf2n.mpg'
#vidFile = 'bbae1a.mpg'
#vidFile='bbae2a.mpg'
#vidFile = 'myvideo.mp4'
#vidFile = 'leftwink.mp4'
#vidFile = 'rightwink.mp4'
#vidFile = 'blink8.avi'
#vidFile = 'grid_corpus_male.mpg'
#vidFile = 'lbbe1s.mpg'
#vidFile = 'blink.mp4'
#vidFile = 'blink8_test_moving_camera.mp4'  
#vidFile = 'blink8_test_NoneError.mp4'
#vidFile = 'blinking with head movements.mp4'
#vidFile = 'with_glasses.mp4'
#vidFile = 'with_head_motion.mp4' # not working none type error
#vidFile = 'with_baby.mp4'
#vidFile = 'blink_test.mp4'
#vidFile = 'head_move.mp4'  #not working
#vidFile = 'new_eyeblink8.mp4'
#vidFile = 'mead001.mp4'
vidFile = 'M07-Joy-Face Forward.mpeg'


detector = dlib.get_frontal_face_detector() #Defines what face detector
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

Video_path = (vidFolder+'/'+vidFile)
PicturePath = (vidFolder+'/pictures/')  # path to store pictures
GaborPath = (vidFolder+'/gabor/') #path to store Gabor features
Gabor_L_EBPath = (vidFolder+'/gabor_l_eyebrow/')  #path to store gabor feature of lefteyebrowss
FramePath = (vidFolder+'/frames/')
SheetPath = (vidFolder+'/sheet/') # path to storSheetPath
FeaturesPath = (vidFolder+'/features/') # path to store sheets

# new variable for shapePoints for right eye, and left eye,nose and mouth can easily add more
shapePoints = [[36, 39, 37, 40], [42, 45, 43, 46], [36, 39, 37, 40], [42, 45, 43, 46],[27, 33, 31, 35], [48, 54, 50, 58]]

# new variable for border params
# left eye, right eye, right eyebrow, left eyebrow, nose ,mouth(arguments, top, bottom,right,left)
borders = [[-5, 5, -5, 5], [-5, 5, -5, 5], [-25, 10, -5, 10], [-25, 10, -5, 10],[-30, 10, -20, 20],[-10,10,-10,10]]

# new array for paths
imgPaths=[]
# store path detail as array
imgPaths.append(vidFolder+'/right_eye/')  # path to store right eye
imgPaths.append(vidFolder+'/left_eye/')  # path to store left eye
imgPaths.append(vidFolder+'/right_eyebrow/') #right eyebrow
imgPaths.append(vidFolder+'/left_eyebrow/')  # Path to store left eyebrow
imgPaths.append(vidFolder+'/Nose/')  # Path to Nose
imgPaths.append(vidFolder+'/Mouth/')  # Path to Mouth
#imgPaths.append(r'C:/Users/Architect Iqra Ayoub/PycharmProjects/MyfirstPro/ProjectOptimised/Project/eye_blinking/')  # Path to store Eye_Blinking
# All above defines folder paths but does not create
# add new variables
frames2.Frame(detector,predictor,shapePoints, borders, Video_path,PicturePath,imgPaths, GaborPath,SheetPath,FeaturesPath,Gabor_L_EBPath)