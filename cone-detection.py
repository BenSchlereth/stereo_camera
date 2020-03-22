"""detects cones in Images"""
import cv2
import numpy as np

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    print(image.shape)
    y1=image.shape[0]
    y2=int(y1*(3/5))
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 100)
    return canny

def colorfilter(image):
    lower_green = np.array([30,100,0])
    upper_green = np.array([70,255,255])
    mask = cv2.inRange(image, lower_green, upper_green)
    res = cv2.bitwise_and(image, image, mask=mask)
    return res



image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
lane_image = np.copy(image)
hsv = cv2.cvtColor(lane_image, cv2.COLOR_RGB2HSV)

filtered_image = colorfilter(hsv)

cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.resizeWindow("result", 600,600)
cv2.imshow("result", filtered_image)
cv2.waitKey(0)
