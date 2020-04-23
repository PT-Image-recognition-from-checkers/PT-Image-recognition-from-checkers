from urllib.request import urlopen

import board
import cv2
import numpy as np

#telefon
url = 'http://192.168.2.8:8080/shot.jpg'

#laptop
#cap = cv2.VideoCapture(0)

while True:
    #telefon
    imgResp = urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, 1)
    dst = board.find_edges_and_perspective_transform(img)
    cv2.imshow('Camera', dst)

    #laptop
    #frame = cap.read()
    #dst = board.find_edges_and_perspective_transform(frame)
    #board.find_checkers(dst)
    #cv2.imshow('Camera', dst)

    if ord('q') == cv2.waitKey(10):
        exit(0)
