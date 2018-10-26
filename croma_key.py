import cv2
import numpy as np


img_src = cv2.imread('example.png')
img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
rgb_min = np.array([[[0, 80, 0]]], np.uint8)
rgb_max = np.array([[[0, 255, 0]]], np.uint8)
hsv_min = cv2.cvtColor(rgb_min, cv2.COLOR_BGR2HSV)[0][0]
hsv_max = cv2.cvtColor(rgb_max, cv2.COLOR_BGR2HSV)[0][0]
mask_inverse = cv2.inRange(img_hsv, hsv_min, hsv_max)
mask = cv2.bitwise_not(mask_inverse)
mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
masked_src = cv2.bitwise_and(img_src, mask_rgb)
img_dest = cv2.addWeighted(masked_src, 1, cv2.cvtColor(mask_inverse, cv2.COLOR_GRAY2RGB), 1, 0)

img_bin = cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY_INV)[1]
img_filtered1 = cv2.GaussianBlur(img_bin, (11, 11), 0)
img_mask = cv2.merge((img_bin, img_filtered1, img_bin))
img_s1m = cv2.bitwise_and(img_src1, img_mask)
img_maskn = cv2.bitwise_not(img_mask)
img_s2m = cv2.bitwise_and(img_src2, img_maskn)
img_dest = cv2.bitwise_or(img_s1m, img_s2m)
img_filtered1 = cv2.blur(img_dest, (2, 2))
img_filtered2 = cv2.GaussianBlur(img_dest, (11, 11), 1)
img_filtered3 = cv2.bilateralFilter(img_dest, 11, 50, 100)
img_filtered4 = cv2.medianBlur(img_dest, 9)

cv2.imwrite('a.jpg', img_dest)
cv2.imwrite('wine_cromakey1.jpg', img_filtered1)
cv2.imwrite('wine_cromakey2.jpg', img_filtered2)
cv2.imwrite('wine_cromakey3.jpg', img_filtered3)
cv2.imwrite('wine_cromakey4.jpg', img_filtered4)
