#!/usr/bin/env python3

import os

import cv2

from nvjpeg import NvJpeg

nj = NvJpeg()
image_file = os.path.join(os.path.dirname(__file__), "test-image", "test.jpg")
print(image_file)
fp = open(image_file, "rb")
img = fp.read()
fp.close()
nj_np = nj.decode(img)
cv_np = cv2.imread(image_file)

cv2.imshow("NvJpeg Decode Image", nj_np)
cv2.imshow("OpenCV Decode Image", cv_np)
cv2.waitKey(0)

nj_jpg = nj.encode(cv_np)

fp = open(os.path.join(os.path.dirname(__file__), "out", "python-nvjpeg-test.jpg"), "wb")
fp.write(nj_jpg)
fp.close()

cv2.imwrite(os.path.join(os.path.dirname(__file__), "out", "python-opencv-test.jpg"), cv_np)

nv_np = nj.read(image_file)
nj.write(os.path.join(os.path.dirname(__file__), "out", "python-nvjpeg-write-test.jpg"), nv_np)
