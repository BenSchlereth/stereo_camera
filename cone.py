class Cone(object):
    def __init__(self):
        """generates an object where all necesarry attributes of cones are saved"""
        self.top_box = []
        self.top_con = []
        self.bottom_box = []
        self.bottom_con = []
        self.distance = -1
        self.left_bottom_corner = [0, 0]
        self.right_top_corner = [0, 0]

    def rectangle(self):
        print(self.top_con)

    def bounding_box(self):
        box_x1 = self.bottom_box[0]
        box_y1 = self.bottom_box[1] + self.bottom_box[3]
        box_x2 = self.bottom_box[0] + self.bottom_box[2]
        box_y2 = self.top_box[1]
        self.left_bottom_corner = box_x1, box_y1
        self.right_top_corner = box_x2, box_y2
        # return self.left_bottom_corner, self.right_top_corner
