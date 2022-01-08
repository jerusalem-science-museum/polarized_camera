#!/usr/bin/python3
#
# polarized_camera code
# arad.rgb@gmail.com 24/11/2021
#
import cv2 # sudo apt install python3-opencv
import numpy as np


CAM_RES = (1280, 720) # (1920, 1080) (640, 480) v4l2-ctl --list-formats-ext
WINDOW_TITLE = 'polarized_camera'
WINDOW_SIZE = (1400, 800) # (1360 , 768)
IMG_POS = [0, 100]
img = cv2.imread('/home/pi/Public/polarized_camera/res/logo0.png', cv2.IMREAD_UNCHANGED)

img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
img_size = img.shape[:2]
IMG_POS[0] = (WINDOW_SIZE[1] - img_size[0]) // 2

#img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
ret, mask = cv2.threshold(img[:, :, 3], 0, 255, cv2.THRESH_BINARY)
img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_RES[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_RES[1])

cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_FREERATIO) # WINDOW_NORMAL
cv2.setWindowProperty(WINDOW_TITLE, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

try:
    while True:
        ret, frame = cam.read()
        if not ret:
            raise IOError
        frame = cv2.resize(frame, WINDOW_SIZE, interpolation=cv2.INTER_AREA)
#        frame = cv2.flip(frame, 1)
        roi = frame[-img_size[0]-IMG_POS[0]:-IMG_POS[0], -img_size[1]-IMG_POS[1]:-IMG_POS[1]]
        roi[np.where(mask)] = 0
        roi += img

        cv2.imshow(WINDOW_TITLE, frame)
        key = cv2.waitKey(1) & 0xff
        if key == 27: # ESC
            break
except KeyboardInterrupt:
    pass

cam.release()
cv2.destroyAllWindows()
