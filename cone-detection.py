"""detects cones in Images"""
import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussionBlur(gray, (5,5), 0)
    canny =cv2.Canny(blur, 50, 150)
    return canny

image = cv2.imread('Messungen\Messung_1\Gerade_links.jpg')

cv2.imshow("result", image)
cv2.waitKey(0)