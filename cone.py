import numpy as np

margin = 8


class Cone(object):
    def __init__(self):
        """generates an object where all necesarry attributes of cones are saved"""
        self.upper_box = []
        self.upper_con = []
        self.lower_box = []
        self.lower_con = []
        # lower box
        self.lower_left_bottom = [0, 0]
        self.lower_right_bottom = [0, 0]
        self.lower_right_top = [0, 0]
        self.lower_left_top = [0, 0]
        # upper box
        self.upper_right_bottom = [0, 0]
        self.upper_left_bottom = [0, 0]
        self.upper_left_top = [0, 0]
        self.upper_right_top = [0, 0]
        # bounding box
        self.bounding_box_top = 0
        self.bounding_box_bottom = 0
        # distance estimations
        self.overall_height = 0
        self.top_part_height = 0

    def upper_bounding_box(self):
        """find the extrem points in all four directions of the upper contour"""
        self.upper_right_bottom[0] = 0
        self.upper_left_bottom[0] = 0
        self.upper_left_top[0] = 0
        self.upper_right_top[0] = 0
        # top and bottom line where the extrem points should lie
        line_top = self.upper_box[1]
        line_bottom = self.upper_box[1] + self.upper_box[3]
        for point in self.upper_con:
            if line_top - margin < point[0][1] < line_top + margin:
                # initalize points
                if self.upper_left_top[0] == 0:
                    self.upper_left_top = point[0]
                    self.upper_right_top = point[0]
                # detect left-top corner
                if point[0][0] < self.upper_left_top[0]:
                    self.upper_left_top = point[0]
                # detect right top corner
                if point[0][0] > self.upper_right_top[0]:
                    self.upper_right_top = point[0]
            if line_bottom - 3 * margin < point[0][1] < line_bottom + 3 * margin:
                if self.upper_left_bottom[0] == 0:
                    self.upper_left_bottom = point[0]
                    self.upper_right_bottom = point[0]
                if point[0][0] < self.upper_left_bottom[0]:
                    self.upper_left_bottom = point[0]
                if point[0][0] > self.upper_right_bottom[0]:
                    self.upper_right_bottom = point[0]

    def lower_bounding_box(self):
        """find the extrem points in all four directions of the lower contour"""
        self.lower_right_bottom[0] = 0
        self.lower_left_bottom[0] = 0
        self.lower_left_top[0] = 0
        self.lower_right_top[0] = 0
        # top and bottom line where the extrem points should lie
        line_top = self.lower_box[1]
        line_bottom = self.lower_box[1] + self.lower_box[3]
        for point in self.lower_con:
            if line_top - margin < point[0][1] < line_top + margin:
                # initalize points
                if self.lower_left_top[0] == 0:
                    self.lower_left_top = point[0]
                    self.lower_right_top = point[0]
                # detect left-top corner
                if point[0][0] < self.lower_left_top[0]:
                    self.lower_left_top = point[0]
                # detect right top corner
                if point[0][0] > self.lower_right_top[0]:
                    self.lower_right_top = point[0]
            if line_bottom - 5 * margin < point[0][1] < line_bottom + 5 * margin:
                if self.lower_left_bottom[0] == 0:
                    self.lower_left_bottom = point[0]
                    self.lower_right_bottom = point[0]
                if point[0][0] < self.lower_left_bottom[0]:
                    self.lower_left_bottom = point[0]
                if point[0][0] > self.lower_right_bottom[0]:
                    self.lower_right_bottom = point[0]

    def bounding_box(self):
        """find the outermost points of the cone"""
        box_x1 = self.lower_box[0]
        box_y1 = self.lower_box[1] + self.lower_box[3]
        box_x2 = self.lower_box[0] + self.lower_box[2]
        box_y2 = self.upper_box[1]
        self.bounding_box_bottom = box_x1, box_y1
        self.bounding_box_top = box_x2, box_y2

    def distance(self):
        """calculate the distance to the cone with different functions"""
        # with overall height
        height = self.lower_box[1] + self.lower_box[3] - self.upper_box[1]
        self.overall_height = (2 * 220) / height  # calibrated for 2m distance
        # print("distance with overall height:   ", self.overall_height, "m")
        # with side length
        side = np.sqrt((self.lower_right_top[0] - self.upper_right_top[0]) ** 2
                       + (self.lower_right_top[1] - self.upper_right_top[1]) ** 2)
        self.top_part_height = 280 / side  # calibrated for 2m distance
        # print("distance with side length: %2.3f m" % self.top_part_height)
