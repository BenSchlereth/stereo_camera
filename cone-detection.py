"""detects cones in Images"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    """returns only the edges"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 100)
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
    blur = cv2.GaussianBlur(res, (5,5), 0)
    return blur, hsv



image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
lane_image = np.copy(image)
filtered_image, converted_image = colorfilter(image)
img1 = cv2.cvtColor(filtered_image, cv2.COLOR_RGB2GRAY)

#template not working properly
img2 = cv2.imread('Messungen/templates/Green-Cone_1.png', cv2.IMREAD_GRAYSCALE) # trainImage
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.imshow(img3),plt.show()



cv2.namedWindow("original",cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 600,600)
cv2.imshow("original", template)
cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.resizeWindow("result", 600,600)
cv2.imshow("result", filtered_image)

cv2.waitKey(0)
