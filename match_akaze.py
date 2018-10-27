import sys
import numpy as np
import cv2

img1 = cv2.imread("./source1.jpg")
img2 = cv2.imread("./source2.png")

akaze = cv2.ORB_create()

kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

bf = cv2.BFMatcher()

matches = bf.knnMatch(des1, des2, k=2)

ratio = 0.8
good = []
for m, n in matches:
	if m.distance < ratio * n.distance:
		good.append([m])

img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
cv2.imwrite('result.jpg', img3)

sys.exit()
