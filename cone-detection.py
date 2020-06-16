"""detects cones in Images"""
import cv2
import numpy as np
import time
from cone import Cone

start_time = time.time()

# size of bounding boxes:
MIN_WIDTH = 10
MIN_HEIGTH = 12


def colorfilter(image):
    """filters a color in a picture"""
    # Converts to HSV Color spectrum
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # value for colorfilter
    lower_green = np.array([45, 100, 0])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    # GaussianBlur with (x,x) is the Pixelsize and will determinate the viewing distance
    blur = cv2.GaussianBlur(res, (15, 15), 0)
    return blur, mask


# Get image
image = cv2.imread('Messungen/Messung_2/Gerade_Links_1080p.jpg')
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

# calculate ratio to search the top part of a cone
cones = []
for con in hull:
    box = cv2.boundingRect(con)
    ratio = box[2] / box[3]
    if 0.6 < ratio < 0.8:
        detected = Cone()
        detected.upper_box = box
        detected.upper_con = con
        cones.append(detected)

# find the bottom part of a cone
for cone in cones:
    min_distance = -1
    for con in hull:
        bounding_box = cv2.boundingRect(con)
        is_below = False
        if (bounding_box[1] - cone.upper_box[1]) > 0:
            is_below = True
        distance = np.sqrt((bounding_box[1] - cone.upper_box[1]) ** 2 + (bounding_box[0] - cone.upper_box[0]) ** 2)
        if min_distance > distance > 0 and is_below or min_distance == -1:
            min_distance = distance
            possible_box = bounding_box
            possible_con = con
    # print("estimation with ratio", (min_distance / cone.upper_box[3] - 1.57) / 0.06, "m")
    # print("estimation with height", (2 * 229) / cone.upper_box[3], "m")
    # y_Koo = possible_box[1] + possible_box[3] - cone.upper_box[1]
    # print("estimation with overall-height", (2 * 708) / y_Koo, "m")
    # print()
    cone.lower_box = possible_box
    cone.lower_con = possible_con

# draw bounding boxes
for cone in cones:
    # cone.bounding_box()
    cone.upper_bounding_box()
    cone.lower_bounding_box()
    cone.distance()
    print("right", cone.lower_right_bottom)
    print("left", cone.lower_left_bottom)
    print()
    x1 = cone.upper_right_bottom[0]
    y1 = cone.upper_right_bottom[1]
    x2 = cone.upper_right_top[0]
    y2 = cone.upper_right_top[1]
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 10)
    cv2.line(image,
             (cone.lower_right_bottom[0], cone.lower_right_bottom[1]),
             (cone.lower_right_top[0], cone.lower_right_top[1]),
             (0, 0, 255),
             10)
    # cv2.rectangle(image, cone.lower_left_bottom, cone.upper_right_top, (0, 0, 255), 10)


print("---%s seconds---" % (time.time() - start_time))

cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 1000, 600)
cv2.imshow("original", image)

cv2.waitKey(0)
