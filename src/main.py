#!/usr/bin/python3
#
# polarized_camera code
# arad.rgb@gmail.com 24/11/2021
#
import cv2 # sudo apt install python3-opencv


CAM_RES = (1280, 720) # (1920, 1080) (640, 480) v4l2-ctl --list-formats-ext
WINDOW_TITLE = 'polarized_camera'
WINDOW_SIZE = (1400, 800)
TEXT = 'Arad and Amir!'
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 3
TEXT_COLOR = (0, 0, 255)
TEXT_THICKNESS = 10
TEXT_LINETYPE = 2
TEXT_SIZE = cv2.getTextSize(TEXT, TEXT_FONT, TEXT_SCALE, TEXT_THICKNESS)[0]
TEXT_BOTTOM_LEFT = ((WINDOW_SIZE[0] - TEXT_SIZE[0]) // 2, TEXT_SIZE[1] + 10)

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
        cv2.putText(frame, TEXT,
            TEXT_BOTTOM_LEFT, TEXT_FONT, TEXT_SCALE,
            TEXT_COLOR, TEXT_THICKNESS, TEXT_LINETYPE)
        cv2.imshow(WINDOW_TITLE, frame)
        key = cv2.waitKey(1) & 0xff
        if key == 27: # ESC
            break
except KeyboardInterrupt:
    pass

cam.release()
cv2.destroyAllWindows()
