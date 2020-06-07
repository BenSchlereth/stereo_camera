"""detects cones in Images"""
import cv2
import numpy as np
import time
start_time = time.time()

# 16MP Camera:
pixel_horizontal = 5376
pixel_vertical = 3024

# size of bounding boxes:
MIN_WIDTH = 30
MIN_HEIGTH = 40


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

# detect contours
img2, contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# find valid contours with hierarchy
foreground_contours = []
for hier, con in zip(hierarchy[0], contours):
    if hier[3] == -1:
        foreground_contours.append(con)

# delete small contours
valid_contours = []
for con in foreground_contours:
    box = cv2.boundingRect(con)
    if box[2] >= MIN_WIDTH and box[3] >= MIN_HEIGTH:
        valid_contours.append(con)

# create hull array for convex hull points
hull = []
for con in valid_contours:
    hull.append(cv2.convexHull(con, True))
cv2.drawContours(image, hull, -1, (255, 0, 0), 8, 8)

# calculate ratio to search for cones
top_part = []
for con in hull:
    box = cv2.boundingRect(con)
    ratio = box[2] / box[3]
    if 0.6 < ratio < 0.8:
        top_part.append(box)
        box_x1 = box[0] - box[2] - 4
        box_y1 = box[1] + int(3 * box[3]) - 4
        box_x2 = box[0] + 2 * box[2] + 4
        box_y2 = box[1] + 4
        cv2.rectangle(image, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 255), 10)


print("---%s seconds---" % (time.time() - start_time))

cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 1000, 600)
cv2.imshow("original", image)

cv2.waitKey(0)
