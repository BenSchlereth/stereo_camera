"""detects cones in Images"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
pixel_horizontal = 5376
pixel_vertical = 3024

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
template_2m = cv2.imread('Messungen/templates/Green-Cone_2.png')
lane_image = np.copy(image)
filtered_image, green_mask = colorfilter(lane_image)

print(green_mask.shape)
print(len(image))

#devide in different views
cutout = np.zeros((1200,pixel_horizontal,3))

cutout[:,:,0] = green_mask[   0:1200,:]
cutout[:,:,1] = green_mask[ 900:2100,:]
cutout[:,:,2] = green_mask[1824:    ,:]
print(cutout[:,:,0].shape)

# #extract cones in Messungen/Messung_1/Gerade_Links.jpg
# cone_2m = green_mask[2200:3000,1650:2200]
# cone_4m = green_mask[1400:1800,1850:2200]
# cone_6m = green_mask[1100:1350,1950:2100]
# cone_8m = green_mask[950:1130,1950:2150]
# cone_10m = green_mask[850:990,2000:2150]
#
# cv2.imwrite("mask_cone_2m.png",cone_2m)
# cv2.imwrite("mask_cone_4m.png",cone_4m)
# cv2.imwrite("mask_cone_6m.png",cone_6m)
# cv2.imwrite("mask_cone_8m.png",cone_8m)
# cv2.imwrite("mask_cone_10m.png",cone_10m)

gray_template_2m = cv2.cvtColor(template_2m, cv2.COLOR_RGB2GRAY)


cv2.namedWindow("original",cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 600,600)
cv2.imshow("original", green_mask)
cv2.namedWindow("cutout_3",cv2.WINDOW_NORMAL)
cv2.resizeWindow("cutout_3", 600,600)
cv2.imshow("cutout_3", cutout[:,:,2])
cv2.namedWindow("result",cv2.WINDOW_NORMAL)
cv2.resizeWindow("result", 600,600)
cv2.imshow("result", cone_2m)

cv2.waitKey(0)
