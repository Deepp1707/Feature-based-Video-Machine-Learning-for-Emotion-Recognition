import glob
import cv2
import os
import extracter
import dlib
import time
import ROI
import TPE
import Gabor
import Features
a=time.time()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#VideoPath = r'../Test video/*.mpg'
#VideoPath ='../Test video/bbae2a.mpg'
VideoPath ='../Test video/bbae2a.mpg'
Frame = '../Test video/pictures/'# path to store pictures
MouthPath = '../Test video/mouth/'  # path to store mouth
GaborPath = '../Test video/Gabor/'#path to store Gabor features
SheetPath = '../Test video/Sheet/' # path to storSheetPath
FeaturesPath = '../Test video/Features/'  # path to store sheets

print("yikes")
extracter.Frame(detector,predictor,VideoPath,Frame,MouthPath,GaborPath,SheetPath,FeaturesPath)


b=time.time()
print("Time = ",b-a)