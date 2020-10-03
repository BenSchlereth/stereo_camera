"""detects cones in Images"""
import cv2
import numpy as np
import time
from cone import Cone

# size of bounding boxes:
MIN_WIDTH = 10
MIN_HEIGTH = 12


def colorfilter(image):
    """filters a color in a picture"""
    # Converts to HSV Color spectrum
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # value for colorfilter
    # lower_green = np.array([45, 100, 0])
    # upper_green = np.array([90, 255, 255])
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([100, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(hsv, hsv, mask=mask)

    # GaussianBlur with (x,x) is the Pixelsize and will determinate the viewing distance
    blur = cv2.GaussianBlur(res, (15, 15), 0)
    return blur, mask


vidcap = cv2.VideoCapture('/home/ben/Videos/GOPR0206.MP4')
vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# save video
# output = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'MPEG'), 20.0, (1280, 720))

if not vidcap.isOpened():
    print("Cannot open camera")
    exit()
success, image = vidcap.read()

for i in range(2600):
    success, image = vidcap.read()

start_time = time.time()
frame = 0
while success:
    frame = frame + 1
    success, image = vidcap.read()
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
        area = cv2.contourArea(con)
        if area * (-(box[1] - 1080)) > 10000:
            valid_contours.append(con)

    # calculate ratio to search the top part of a cone
    cones = []
    for con in valid_contours:
        box = cv2.boundingRect(con)
        ratio = box[2] / box[3]
        if 0.6 < ratio < 0.8:
            detected = Cone()
            detected.upper_box = box
            detected.upper_con = con
            cones.append(detected)

    # find the bottom part of a cone
    delete = []
    for cone in cones:
        min_distance = 3.5 * cone.upper_box[3]  # initial distance
        possible_box = [0, 0, 0, 0]
        possible_con = [[[0]]]
        area_top = cv2.contourArea(cone.upper_con)
        for con in valid_contours:
            bounding_box = cv2.boundingRect(con)
            area_bottom = cv2.contourArea(con)
            # bounding box is to the left and below
            if bounding_box[0] < cone.upper_box[0] and bounding_box[1] > cone.upper_box[1]:
                distance = np.sqrt((bounding_box[1] - cone.upper_box[1]) ** 2
                                   + (bounding_box[0] - cone.upper_box[0]) ** 2)
                if min_distance > distance > 0:
                    min_distance = distance
                    possible_box = bounding_box
                    possible_con = con
        cone.lower_box = possible_box
        cone.lower_con = possible_con
        if cone.lower_con[0][0][0] == 0 or cone.lower_box[0] == 0:
            delete.append(cone)

    for cone in delete:
        cones.remove(cone)

    # draw bounding boxes
    for cone in cones:
        # cone.bounding_box()
        cone.upper_bounding_box()
        cone.lower_bounding_box()
        cone.bounding_box()
        cone.distance()
        x1 = cone.upper_right_bottom[0]
        y1 = cone.upper_right_bottom[1]
        x2 = cone.upper_right_top[0]
        y2 = cone.upper_right_top[1]
        # draw side-lines
        # cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 10)
        # cv2.line(image,
        #          (cone.lower_right_bottom[0], cone.lower_right_bottom[1]),
        #          (cone.lower_right_top[0], cone.lower_right_top[1]),
        #          (0, 0, 255),
        #          10)

        # draw bounding box
        cv2.rectangle(image, cone.bounding_box_bottom, cone.bounding_box_top, (0, 0, 255), 10)
        # add text
        dis = str(round(cone.top_part_height, 2))
        cv2.putText(image, dis, cone.bounding_box_top, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # break-key
    if cv2.waitKey(10) == 27 or frame > 400:
        break

    cv2.imshow('frame', image)
    # output.write(frame)

vidcap.release()
# output.release()
cv2.destroyAllWindows()
# measure time
print(frame)
print("---%s seconds---" % (time.time() - start_time))

# cv2.namedWindow("original", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("original", 1000, 600)
# cv2.imshow("original", image)
# cv2.waitKey(0)
