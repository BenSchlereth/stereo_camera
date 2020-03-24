"""detects cones in Images"""
import cv2
import numpy as np

def canny(image):
    """returns only the edges"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 100)
    return canny

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
    blur = cv2.GaussianBlur(res, (5,5), 0)
    return blur, hsv



image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
lane_image = np.copy(image)

filtered_image, converted_image = colorfilter(image)

cv2.namedWindow("original",cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 600,600)
cv2.imshow("original", lane_image)
cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.resizeWindow("result", 600,600)
cv2.imshow("result", filtered_image)

cv2.waitKey(0)
