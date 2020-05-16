"""detects cones in Images"""
import cv2
import numpy as np
# from matplotlib import pyplot as plt

# 16MP Camera:
pixel_horizontal = 5376
pixel_vertical = 3024


def extracting_cones_16MP(image):
    """extract cones in Messungen/Messung_1/Gerade_Links.jpg"""
    cone_2m = image[2200:3000, 1650:2200]
    cone_4m = image[1400:1800, 1850:2200]
    cone_6m = image[1100:1350, 1950:2100]
    cone_8m = image[950:1130, 1950:2150]
    cone_10m = image[850:990, 2000:2150]

    cv2.imwrite("Messungen/templates/image_cone_2m.png", cone_2m)
    cv2.imwrite("Messungen/templates/image_cone_4m.png", cone_4m)
    cv2.imwrite("Messungen/templates/image_cone_6m.png", cone_6m)
    cv2.imwrite("Messungen/templates/image_cone_8m.png", cone_8m)
    cv2.imwrite("Messungen/templates/image_cone_10m.png", cone_10m)


def canny(image):
    """returns only the edges"""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 20, 20)
    return canny


def colorfilter(image):
    """filters a color in a picture"""
    # Converts to HSV Color spectrum
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # value for colorfilter
    lower_green = np.array([30, 100, 0])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    # GaussianBlur with (x,x) is the Pixelsize and will determinate the viewing distance
    blur = cv2.GaussianBlur(res, (15, 15), 0)
    return blur, mask


# Get image
image = cv2.imread('Messungen/Messung_1/Gerade_Links.jpg')
filtered_image, green_mask = colorfilter(image)
filtered_gray = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2GRAY)

# Get Templates
template_2m = cv2.imread('Messungen/templates/image_cone_2m.png', 0)
template_4m = cv2.imread('Messungen/templates/image_cone_4m.png', 0)
template_6m = cv2.imread('Messungen/templates/image_cone_6m.png', 0)
template_8m = cv2.imread('Messungen/templates/image_cone_8m.png', 0)
template_10m = cv2.imread('Messungen/templates/image_cone_10m.png', 0)

# detect contours
img2, contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (255, 0, 0), 3)

# # devide in different views
# #cutout = np.zeros((1200,pixel_horizontal,3))
# #cutout[:,:,0] = filtered_gray[   0:1200,:] #backround
# #cutout[:,:,1] = filtered_gray[ 900:2100,:]
# #cutout[:,:,2] = filtered_gray[1824:    ,:] #foreground
# back = filtered_gray[0:1200, :]     # backround
# middle = filtered_gray[900:2100, :]
# front = filtered_gray[1800:, :]     # foreground
#
# # Apply template Matching
# res = cv2.matchTemplate(front, template_2m, cv2.TM_CCORR)
# w, h = template_2m.shape[::-1]
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
# cv2.rectangle(front, top_left, bottom_right, 255, 2)
#
# res = cv2.matchTemplate(middle, template_4m, cv2.TM_CCORR)
# w, h = template_4m.shape[::-1]
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
# cv2.rectangle(middle, top_left, bottom_right, 255, 2)
#
# res = cv2.matchTemplate(back, template_6m, cv2.TM_CCORR)
# w, h = template_6m.shape[::-1]
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
# cv2.rectangle(back, top_left, bottom_right, 255, 2)
#
# # to binary image
# _, thresh_img = cv2.threshold(filtered_gray,75,255,cv2.THRESH_BINARY)
# _, thresh_back = cv2.threshold(back,75,255,cv2.THRESH_BINARY)
# _, thresh_middle = cv2.threshold(middle,75,255,cv2.THRESH_BINARY)
# _, thresh_front = cv2.threshold(front,75,255,cv2.THRESH_BINARY)
#
#
# #Converting image Back
# converted_image = np.zeros((pixel_vertical,pixel_horizontal))
# converted_image[0:900,:] = thresh_back[0:900,:]
# #Overlay between back and middle
# overlay = cv2.bitwise_or(thresh_back[900:,:],thresh_middle[0:300,:])
# converted_image[900:1200,:]=overlay
# converted_image[1200:1800,:] = thresh_middle[300:900,:]
# #Overlay between middle and back
# overlay = cv2.add(thresh_middle[900:,:],thresh_front[0:300,:])
# converted_image[1800:2100,:] = overlay
# converted_image[2100:,:] = thresh_front[300:,:]
#
# plt.subplot(121), plt.imshow(res, cmap='gray')
# plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
# plt.subplot(122), plt.imshow(converted_image, cmap='gray')
# plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
# plt.suptitle("matching")
# plt.show()

cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 1000, 600)
cv2.imshow("original", img2)
cv2.namedWindow("template", cv2.WINDOW_NORMAL)
cv2.resizeWindow("template", 1000, 600)
cv2.imshow("template", image)

cv2.waitKey(0)
