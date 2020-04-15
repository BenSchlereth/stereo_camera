"""detects cones in Images"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 16MP Camera:
pixel_horizontal = 5376
pixel_vertical = 3024

def extracting_cones_16MP(image):
    """extract cones in Messungen/Messung_1/Gerade_Links.jpg"""
    cone_2m = image[2200:3000,1650:2200]
    cone_4m = image[1400:1800,1850:2200]
    cone_6m = image[1100:1350,1950:2100]
    cone_8m = image[950:1130,1950:2150]
    cone_10m = image[850:990,2000:2150]

    cv2.imwrite("Messungen/templates/image_cone_2m.png", cone_2m)
    cv2.imwrite("Messungen/templates/image_cone_4m.png", cone_4m)
    cv2.imwrite("Messungen/templates/image_cone_6m.png", cone_6m)
    cv2.imwrite("Messungen/templates/image_cone_8m.png", cone_8m)
    cv2.imwrite("Messungen/templates/image_cone_10m.png", cone_10m)

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
template_2m = cv2.imread('Messungen/templates/image_cone_2m.png', 0)
filtered_image, green_mask = colorfilter(image)
filtered_gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

#devide in different views
#cutout = np.zeros((1200,pixel_horizontal,3))
#cutout[:,:,0] = filtered_gray[   0:1200,:] #backround
#cutout[:,:,1] = filtered_gray[ 900:2100,:]
#cutout[:,:,2] = filtered_gray[1824:    ,:] #foreground

# Apply template Matching
res = cv2.matchTemplate(filtered_gray, template_2m, cv2.TM_CCORR)
w, h = template_2m.shape[::-1]
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(filtered_gray, top_left, bottom_right, 255, 2)

plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(filtered_gray,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle("matching")
plt.show()

#cv2.namedWindow("original",cv2.WINDOW_NORMAL)
#cv2.resizeWindow("original", 600,600)
#cv2.imshow("original", filtered_gray)
#cv2.namedWindow("template",cv2.WINDOW_NORMAL)
#cv2.resizeWindow("template", 600,600)
#cv2.imshow("template", template_2m)

cv2.waitKey(0)
