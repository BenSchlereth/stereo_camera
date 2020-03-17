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
    gray = (np.float32(imgUMat), cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussionBlur(gray, (5,5), 0)
    canny =cv2.Canny(blur, 50, 150)
    return canny

image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
lane_image = np.copy(image)

cv2.imshow("result", lane_image)
cv2.waitKey(0)
