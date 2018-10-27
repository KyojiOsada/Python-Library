import sys
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

img_gray1 = cv2.imread("../img/note_quater1.jpg", 0)
img_rgb2 = cv2.imread("../img/score_kaerunouta.png")
img_gray2 = cv2.cvtColor(img_rgb2, cv2.COLOR_BGR2GRAY)

ret, img_bin1 = cv2.threshold(img_gray1, 127, 255, cv2.THRESH_BINARY_INV)
ret, img_bin2 = cv2.threshold(img_gray2, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite('img_bin1.png', img_bin2)

# Sobel
img_sobel = cv2.Sobel(img_bin2, cv2.CV_64F, 0, 1, ksize=1)
img_abs = cv2.convertScaleAbs(img_sobel)
cv2.imwrite('img_sobel1.png', img_abs)

# Canny
img_canny = cv2.Canny(img_bin2, 200, 200)
cv2.imwrite('img_canny1.png', img_canny)

# Hough
lines = cv2.HoughLinesP(img_bin2, rho=5, theta=math.pi / 180.0 * 90, threshold=200, minLineLength=30, maxLineGap=5)
if lines is not None:
	for (x1, y1, x2, y2) in lines[0]:
		img_hough = cv2.line(img_gray2, (x1, y1), (x2, y2), (0, 0, 255), 1)
else:
	print('No')

cv2.imwrite('img_hough1.png', img_hough)

sys.exit()
