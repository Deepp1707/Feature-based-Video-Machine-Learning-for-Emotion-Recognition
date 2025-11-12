import glob
import cv2
import os

import scipy.ndimage as ndi
import pylab as pl
import matplotlib.patches as mpatches
from PIL import Image
import sys
from xlwt import *
import xlwt


from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from skimage import io,measure,color,data,filters
import matplotlib.image as mpimg
#import roi
from matplotlib import pyplot as plt
from openpyxl import Workbook

import roi_v2
#import r_eye
#import r_eyebrow
#import l_eyebrow
workbook = Workbook()
sheet = workbook.active


# file = xlwt.Workbook()
# sheet = file.add_sheet('Sheet1', cell_overwrite_ok=True)
#sheet = file.active
#cols = ["A", "B", "C", "D", "E"]
#txt = [0,1,2,3,4]
sheet["A1"] = "Frame no"
sheet["B1"] = "Blink Ratio"
sheet["C1"] = "Left Eye ratio"
sheet["D1"] = "Right Eye Ratio"
# sheet.write('A1', 'Frame No')
# sheet.write('B1', 'Blink Ratio')
# sheet.write('C1', 'Left Eye Ratio')
# sheet.write('D1', 'Right Eye ratio')





def Frame(detector,predictor, shapePoints, borders, Video_path,PicturePath,imgPaths,GaborPath,SheetPath,FeaturesPath,Gabor_L_EBPath):
 # Frame, function that does everything
 #print('in frame')

 if not os.path.exists(PicturePath):
        # creates picture folder
        os.mkdir(os.path.join(PicturePath))




 # for each video in folder
 for video in glob.glob(Video_path): # path of videos
    (filepath, tempfilename) = os.path.split(video)
    (shotname, extension) = os.path.splitext(tempfilename)
    folder_name = shotname
    # Creates path for individual video
    Path = os.path.join(PicturePath, folder_name)
    if not os.path.exists(Path):
        os.mkdir(Path)

    if not os.path.exists(SheetPath):
        os.mkdir(os.path.join(SheetPath))

    cur_dir = os.path.join(SheetPath, shotname)
    if not os.path.exists(cur_dir):
        os.mkdir(cur_dir)

    # reads video and stores in cap variable
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # size=(960,544)
    # print ('size', size)

    # Create empty list for frames and for values
    # Note, create it OUTSIDE loop, so it doesn't get overwritten
    v_eyeFrame = []
    v_eyeBlink = []
    v_eyeLeft = []
    v_eyeRight = []



    # for each frame in cap, read
    i = 0
    while (cap.isOpened()):  # cv2.VideoCapture.isOpened()
        i = i + 1
        ret, frame = cap.read()  # cv2.VideoCapture.read()　
        if ret == True:
            path = Path +'/'
            picturepath = path+ str('%02d' % i) + '.jpg'
            #print (picturepath)

            # Writes all raw pictures to file
            cv2.imwrite(picturepath, frame)

            # Save duplication by just calling detector once
            dets = detector(frame, 1)
            lenDets = len(dets)

            if(lenDets>0):
                for featCount in range(len(shapePoints)):
                    #print ("frame is ", i)

                    #print(len(dets))

                # Extracts right eye and gabor of feature
                # do this for each frame
                #print('inside a frame')
                # Modify the call to return 2 values
                    (framOut,blinkOut,left_eyeratio,right_eyeratio) = roi_v2.rect1(predictor, i, shotname, picturepath, imgPaths[featCount], GaborPath, SheetPath, FeaturesPath,
                                                  shapePoints[featCount], borders[featCount], frame, dets)

                #append values to list
                v_eyeFrame.append(framOut)
                v_eyeBlink.append(blinkOut)
                v_eyeLeft.append(left_eyeratio)
                v_eyeRight.append(right_eyeratio)

                # parameters = ['Frame_No', 'Blink_Ratio', 'Left_Eye_ratio', 'Right_Eye_Ratio']
                #
                # value = [framOut, blinkOut, left_eyeratio, right_eyeratio]
                #
                # for j in range(0, len(parameters)):
                #     table.write(j, 0, str(parameters[j]))
                #
                # # 填入第二列
                # for k in range(0, len(value)):
                #     table.write(k, 1, float(value[k]))



                for j in range(len(v_eyeFrame)):


                    sheet['A' + str(j + 2)].value = v_eyeFrame[j] # Frame values
                    sheet['B' + str(j + 2)].value = v_eyeBlink[j] # eye blink ratio
                    sheet['C' + str(j + 2)].value = v_eyeLeft[j]  # left eye ratio
                    sheet['D' + str(j + 2)].value = v_eyeRight[j]  # right eye ratio




            else:
                v_eyeFrame.append(framOut)
                v_eyeBlink.append(2.5)
                v_eyeLeft.append(3.5)
                v_eyeRight.append(3.5)
                #continue

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        else:
            break

    #file.save(cur_dir + '/' + str('%02d') + '.xls')
    #workbook.save(filename="try.xlsx")
    workbook.save(cur_dir + '/'+ shotname +".xlsx")

        #     sheet['F' + str(i + 6)].value = v_eyeBlink[i]
        #     sheet['G' + str(i + 6)].value = v_eyeLeft[i]
        #     sheet['H' + str(i + 6)].value = v_eyeRight[i]
        #
        # wb.save('Frame_estimation.xlsx')
         #wb.save(cur_dir + '/' + 'Frame_estimation.xlsx')





    cap.release()

    print(v_eyeBlink)
    print(v_eyeFrame)
    print(v_eyeLeft)
    print(v_eyeRight)
    fig, ax = plt.subplots()
    #ax.set_xticks(v_eyeFrame, minor=True)
    ax.plot(v_eyeFrame, v_eyeLeft,v_eyeRight)
    ax.plot(v_eyeFrame, v_eyeBlink)
    plt.show()