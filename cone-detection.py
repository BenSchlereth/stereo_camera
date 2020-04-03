"""detects cones in Images"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    """returns only the edges"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 20, 20)
    return canny

#def template():
#    """returns the Template for a green cone in HSV colorspace"""

def colorfilter(image):
    """filters a color in a picture"""
    # Converts to HSV Color spectrum
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # value for colorfilter
    lower_green = np.array([30,100,0])
    upper_green = np.array([90,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    # GaussianBlur with (x,x) is the Pixelsize and will determinate the viewing distance
    blur = cv2.GaussianBlur(res, (15,15), 0)
    return blur, mask



image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
template = cv2.imread('Messungen/templates/Green-Cone_2.png')
lane_image = np.copy(image)
filtered_image, green_mask = colorfilter(lane_image)
gray_image = cv2.cvtColor(filtered_image, cv2.COLOR_RGB2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)

# Threshold image
_,im_match = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
_,template_match = cv2.threshold(gray_template, 128, 255, cv2.THRESH_BINARY)

d2 = cv2.matchShapes(im_match,template_match,cv2.CONTOURS_MATCH_I2,0)
print(d2)

canny_image = canny(filtered_image)

cv2.namedWindow("original",cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 600,600)
cv2.imshow("original", lane_image)
cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.resizeWindow("result", 600,600)
cv2.imshow("result", canny_image)

cv2.waitKey(0)
