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
    """filters a color in a picture"""
    # Converts to HSV Color
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # value for colorfilter
    lower_green = np.array([30,100,0])
    upper_green = np.array([70,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    # GaussianBlur with (x,x) is the Pixelsize and will determinate the viewing distance
    blur = cv2.GaussianBlur(res, (5,5), 0)
    return blur



image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
lane_image = np.copy(image)

filtered_image = colorfilter(lane_image)

cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.resizeWindow("result", 600,600)
cv2.imshow("result", filtered_image)
cv2.waitKey(0)
