import base64
from nvjpeg import NvJpeg
import cv2

nj = NvJpeg()
img = cv2.imread("tests/test-image/test.jpg")
a = base64.b64encode(nj.encode(img)).decode()
print(a)
