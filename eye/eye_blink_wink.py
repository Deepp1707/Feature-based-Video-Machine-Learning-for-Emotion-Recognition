# -----Step 1: Use VideoCapture in OpenCV-----
import cv2
import dlib
import math
import numpy as np
import matplotlib.pyplot as plt

BLINK_RATIO_THRESHOLD = 1.7


 #Getting to know blink ratio

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

    center_top = midpoint(facial_landmarks.part(eye_points[1]),
                          facial_landmarks.part(eye_points[3]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[9]),
                             facial_landmarks.part(eye_points[10]))

    # calculating distance
    horizontal_length = euclidean_distance(corner_left, corner_right)
    vertical_length = euclidean_distance(center_top, center_bottom)

    ratio = horizontal_length / vertical_length

    return ratio

#video path
cap = cv2.VideoCapture("C:/Users/User/OneDrive/code/eyeblink/new_eyeblink8.mp4")
#using webcam
#cap = cv2.VideoCapture(0)
# name of the display window in OpenCV

cv2.namedWindow('BlinkDetector')

# Face detection with dlib-----
detector = dlib.get_frontal_face_detector()

# Detecting Eyes using landmarks in dlib-----
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# these landmarks are based on the image above
left_eye_landmarks = [17,18,19,20,21, 39, 40, 41,36,37, 38]
right_eye_landmarks = [22,23,24,25,26,27, 45, 46, 47, 42, 43, 44]
eye_blink_signal=[]
previous_ratio    = 100
count = 1
total = 0

frame_path = 'C:/Users/User/OneDrive/code/eyeblink/eyes'

i = 0

while True:
    # capturing frame
    retval, frame = cap.read()
    print("starting capture")
    # exit the application if frame not found
    if not retval:
        print("Can't receive frame (stream end?). Exiting ...")
        break

        #converting image to grayscale-----
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(frame_path + str(i) + '.jpg', frame)
    i = i+1

    # Face detection with dlib-----
    # detecting faces in the frame
    faces, _, _ = detector.run(image=frame, upsample_num_times=0,
                               adjust_threshold=0.0)

    # Detecting Eyes using landmarks in dlib-----
    for face in faces:

        landmarks = predictor(frame, face)

        # Calculating blink ratio for one eye-----
        left_eye_ratio = get_blink_ratio(left_eye_landmarks, landmarks)
        right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
        blink_ratio = (left_eye_ratio + right_eye_ratio) / 2
        x = [0]
        y = [0]

        if blink_ratio >= BLINK_RATIO_THRESHOLD:
            print(blink_ratio, "blink")
            count+= 1
        # elif left_eye_ratio and right_eye_ratio <  BLINK_RATIO_THRESHOLD:
        #     count += 1
        #     x.append(1)
        #     print(blink_ratio, "unblink")
        elif blink_ratio >=  BLINK_RATIO_THRESHOLD  and right_eye_ratio < BLINK_RATIO_THRESHOLD:
            print(left_eye_ratio, "Right eye wink")
            total += 1

        elif blink_ratio >=  BLINK_RATIO_THRESHOLD  and left_eye_ratio < BLINK_RATIO_THRESHOLD:
            print(left_eye_ratio, "Left eye wink")
            total += 1

        else:
            if blink_ratio <  BLINK_RATIO_THRESHOLD:
                print(blink_ratio, " AU 45 detected, blink counts")
                total += 1
                y.append(0)

            count = 1



        # Blink detected! Do Something!
            cv2.putText(frame, "Blink Count: {}".format(total), (5, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 1,cv2.LINE_AA)



    cv2.imshow('BlinkDetector', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break






    #blink_graph = numpy.arange(0,5,2.5)
# releasing the VideoCapture object
cap.release()
#print(BLINK_RATIO_THRESHOLD)
# eye_blink_signal = []
# eye_blink_signal.append(blink_ratio)
# plt.plot(eye_blink_signal)
# plt.show()
cv2.destroyAllWindows()

# #plt.style.use('ggplot')
# #count_value = total
# #blinking_ratio = blink_ratio
# #plt.bar(count_value, blinking_ratio, count, color='red')
# # plt.xlabel("blink count")
# # plt.ylabel('E aspect Ratio')
# # plt.title('Horizontal Bar Plot')
# #plt.plot(x,y)
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
#
# # giving a title to my graph
# plt.title('My first graph!')
# plt.plot(x,y)
# plt.show()







#import cv2
# import dlib
#
# #path of the video
# cap = cv2.VideoCapture("C:/Users/User/OneDrive/code/eyeblink/new_eyeblink8.mp4")
#
# #name of the display window in open cv
# cv2.namedWindow("Eye Blink Detection")
# frame_path = r'C:/Users/User/OneDrive/code/Emotion-recognition/framepath'
# #------Step 3: Face detection with dlib------
# detector = dlib.get_frontal_face_detector()
# #-----Step 4: Detecting Eyes using landmarks in dlib-----
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# #these landmarks are based on the image above
# left_eye_landmarks = [36, 37, 38, 39, 40, 41]
# right_eye_landmarks = [42, 43, 44, 45, 46, 47]
#
# i=0
# while True:
#     retval, frame = cap.read()
#
#     #Exit the application if frame doesnot found
#     if not retval:
#         print("cant receive frame(stream end?).Exiting....")
#         break
#         # ------Step 2: converting image to grayscale------
#         frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#
#         # ------Step 3: Face detection with dlib----
#         # detecting faces in the frame
#         faces, _, _ = detector.run(image=frame, upsample_num_times=0,
#                                    adjust_threshold=0.0)
#
#         # -----Step 4: Detecting Eyes using landmarks in dlib-----
#         for face in faces:
#             landmarks = predictor(frame, face)
#             point = (landmarks.part(36).x, landmarks.part(36).y)
#
#         cv2.Imshow('BlinkDetector', frame)
#         key = cv2.waitkey(1)
#         if key == 27:
#             break
#         cv2.imwrite(frame_path + str(i) + '.jpg', frame)
#         i += 1
#
#             #releasing the video
# cap.release()
# cv2.waitKey(0)
# cv2.destroyAllWindows()