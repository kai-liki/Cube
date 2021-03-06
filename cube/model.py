import random
import struct

CENTER = 0
EDGE = 1
CORNER = 2

#  Right hand
#
# Y ^   * Z (Point to the inside of screen)
#   |  /
#   | /
#   *-------> X
#
# A position will be presented as (X, Y, Z). Eg. (1, 1, 1) is the most left front corner.
#

# Axis
X = 0
Y = 1
Z = 2

# Positions
X1 = 0
X2 = 1
X3 = 2
Y1 = 0
Y2 = 1
Y3 = 2
Z1 = 0
Z2 = 1
Z3 = 2


#            GREEN(BACK)
#            RED(TOP)
# BLUE(LEFT) WHITE(FRONT) YELLOW(RIGHT)
#            ORANGE(BOTTOM)
NONE = -1
WHITE = 0
BLUE = 1
ORANGE = 2
GREEN = 3
RED = 4
YELLOW = 5

COLORS = ('W', 'B', 'O', 'G', 'R', 'Y')

# Surface
FRONT = 0   # WHITE
LEFT = 1    # BLUE
BOTTOM = 2  # ORANGE
BACK = 3    # GREEN
TOP = 4     # RED
RIGHT = 5   # YELLOW

# Box rotate mapping. Eg. (TOP, LEFT) means TOP color become to LEFT color
ROTATE_XY = [
    (TOP, RIGHT),
    (RIGHT, BOTTOM),
    (BOTTOM, LEFT),
    (LEFT, TOP),
]

ROTATE_YX = [
    (TOP, LEFT),
    (LEFT, BOTTOM),
    (BOTTOM, RIGHT),
    (RIGHT, TOP)
]

ROTATE_YZ = [
    (TOP, FRONT),
    (FRONT, BOTTOM),
    (BOTTOM, BACK),
    (BACK, TOP)
]

ROTATE_ZY = [
    (TOP, BACK),
    (BACK, BOTTOM),
    (BOTTOM, FRONT),
    (FRONT, TOP)
]

ROTATE_XZ = [
    (FRONT, LEFT),
    (LEFT, BACK),
    (BACK, RIGHT),
    (RIGHT, FRONT)
]

ROTATE_ZX = [
    (FRONT, RIGHT),
    (RIGHT, BACK),
    (BACK, LEFT),
    (LEFT, FRONT)
]

# Direction
# "-" means anticlockwise.
# Else means clockwise.
F = 1
B = 2
R = 3
L = 4
U = 5
D = 6
F_ = -1
B_ = -2
R_ = -3
L_ = -4
U_ = -5
D_ = -6

DIRECTION_OFFSET = 6
# Direction + DIRECTION_OFFSET
DIRECTIONS = [
    'D-',  # 0
    'U-',  # 1
    'L-',  # 2
    'R-',  # 3
    'B-',  # 4
    'F-',  # 5
    '0',   # 6
    'F',   # 7
    'B',   # 8
    'R',   # 9
    'L',   # 10
    'U',   # 11
    'D',   # 12
]

# Direction axis mapping
DirectionToAxis = {
    # Direction : Axis, Axis position, Direction, (Other 2 axis), [Edge position list in REVERSE], [Corner position list in REVERSE]
    F: (Z, Z1, F, (X, Y), ((X2, Y1), (X3, Y2), (X2, Y3), (X1, Y2)), ((X1, Y1), (X3, Y1), (X3, Y3), (X1, Y3)), ROTATE_YX),
    B: (Z, Z3, B, (X, Y), ((X1, Y2), (X2, Y3), (X3, Y2), (X2, Y1)), ((X1, Y3), (X3, Y3), (X3, Y1), (X1, Y1)), ROTATE_XY),
    L: (X, X1, L, (Y, Z), ((Y2, Z1), (Y3, Z2), (Y2, Z3), (Y1, Z2)), ((Y1, Z1), (Y3, Z1), (Y3, Z3), (Y1, Z3)), ROTATE_ZY),
    R: (X, X3, R, (Y, Z), ((Y2, Z1), (Y1, Z2), (Y2, Z3), (Y3, Z2)), ((Y1, Z1), (Y1, Z3), (Y3, Z3), (Y3, Z1)), ROTATE_YZ),
    D: (Y, Y1, D, (X, Z), ((X2, Z1), (X1, Z2), (X2, Z3), (X3, Z2)), ((X1, Z1), (X1, Z3), (X3, Z3), (X3, Z1)), ROTATE_XZ),
    U: (Y, Y3, U, (X, Z), ((X2, Z1), (X3, Z2), (X2, Z3), (X1, Z2)), ((X1, Z1), (X3, Z1), (X3, Z3), (X1, Z3)), ROTATE_ZX),
    F_: (Z, Z1, F_, (X, Y), ((X1, Y2), (X2, Y3), (X3, Y2), (X2, Y1)), ((X1, Y3), (X3, Y3), (X3, Y1), (X1, Y1)), ROTATE_XY),
    B_: (Z, Z3, B_, (X, Y), ((X2, Y1), (X3, Y2), (X2, Y3), (X1, Y2)), ((X1, Y1), (X3, Y1), (X3, Y3), (X1, Y3)), ROTATE_YX),
    L_: (X, X1, L_, (Y, Z), ((Y2, Z1), (Y1, Z2), (Y2, Z3), (Y3, Z2)), ((Y1, Z1), (Y1, Z3), (Y3, Z3), (Y3, Z1)), ROTATE_YZ),
    R_: (X, X3, R_, (Y, Z), ((Y2, Z1), (Y3, Z2), (Y2, Z3), (Y1, Z2)), ((Y1, Z1), (Y3, Z1), (Y3, Z3), (Y1, Z3)), ROTATE_ZY),
    D_: (Y, Y1, D_, (X, Z), ((X2, Z1), (X3, Z2), (X2, Z3), (X1, Z2)), ((X1, Z1), (X3, Z1), (X3, Z3), (X1, Z3)), ROTATE_ZX),
    U_: (Y, Y3, U_, (X, Z), ((X2, Z1), (X1, Z2), (X2, Z3), (X3, Z2)), ((X1, Z1), (X1, Z3), (X3, Z3), (X3, Z1)), ROTATE_XZ),
}


def build_position(axis1, axis1_pos, axis2, axis2_pos, axis3, axis3_pos):
    position = [0, 0, 0]
    position[axis1] = axis1_pos
    position[axis2] = axis2_pos
    position[axis3] = axis3_pos
    return tuple(position)


def build_box(position, colors):
    count_2 = 0
    for i in position:
        if i == 2:
            count_2 = count_2 + 1
    if count_2 == 0:
        return Box(position, CORNER, colors)
    elif count_2 == 1:
        return Box(position, EDGE, colors)
    else:
        return Box(position, CENTER, colors)


class Box:
    def __init__(self, position, position_type, colors):
        self.position = position
        self.colors = colors
        self.type = position_type

    def get_surface_color(self, surface):
        return self.colors[surface]

    def set_surface_color(self, surface, color):
        self.colors[surface] = color

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def validate_transform(self, direction):
        if (direction in (L, L_) and self.position[X] != X1) or \
            (direction in (R, R_) and self.position[X] != X3) or \
            (direction in (U, U_) and self.position[Y] != Y3) or \
            (direction in (D, D_) and self.position[Y] != Y1) or \
            (direction in (F, F_) and self.position[Z] != Z1) or \
                (direction in (B, B_) and self.position[Z] != Z3):
            raise Exception("Invalid transformation %s for box (%s, %s, %s)." %
                            (direction, self.position[X], self.position[Y], self.position[Z]))
        return True

    def rotate_color(self, rotate_mapping):
        first_surface = rotate_mapping[0][0]
        first_surface_color = self.get_surface_color(first_surface)
        for j in range(0, 3):
            from_surface = rotate_mapping[j][0]
            to_surface = rotate_mapping[j][1]
            self.set_surface_color(from_surface, self.get_surface_color(to_surface))
        self.set_surface_color(rotate_mapping[3][0], first_surface_color)


class Cube:

    def __init__(self):
        self.boxes = self.construct_standard()
        self.feature = self.calculate_feature()
        self.standard_string = self.calculate_feature_string(self.feature)
        self.feature_string = self.standard_string

    def construct_standard(self):
        boxes = {}
        for x in (X1, X2, X3):
            for y in (Y1, Y2, Y3):
                for z in (Z1, Z2, Z3):
                    colors = [NONE, NONE, NONE, NONE, NONE, NONE]
                    if x == X1:
                        colors[LEFT] = LEFT
                    if x == X3:
                        colors[RIGHT] = RIGHT
                    if y == Y1:
                        colors[BOTTOM] = BOTTOM
                    if y == Y3:
                        colors[TOP] = TOP
                    if z == Z1:
                        colors[FRONT] = FRONT
                    if z == Z3:
                        colors[BACK] = BACK
                    boxes[(x, y, z)] = build_box([x, y, z], colors)
        return boxes

    def get_box(self, position):
        return self.boxes[position]

    def set_box(self, position, box):
        self.boxes[position] = box

    def rotate(self, axis, axis_position, rest_axis, reversed_rotate_position_list, rotate_mapping):
        tmp_position = build_position(axis,
                                      axis_position,
                                      rest_axis[0],
                                      reversed_rotate_position_list[0][0],
                                      rest_axis[1],
                                      reversed_rotate_position_list[0][1])
        tmp_box = self.get_box(tmp_position)
        for i in range(0, 3):
            cur_position = build_position(axis,
                                          axis_position,
                                          rest_axis[0],
                                          reversed_rotate_position_list[i][0],
                                          rest_axis[1],
                                          reversed_rotate_position_list[i][1])
            next_position = build_position(axis,
                                           axis_position,
                                           rest_axis[0],
                                           reversed_rotate_position_list[i + 1][0],
                                           rest_axis[1],
                                           reversed_rotate_position_list[i + 1][1])
            next_box = self.get_box(next_position)
            next_box.set_position(cur_position)
            self.set_box(cur_position, next_box)
            next_box.rotate_color(rotate_mapping)

        last_position = build_position(axis,
                                       axis_position,
                                       rest_axis[0],
                                       reversed_rotate_position_list[3][0],
                                       rest_axis[1],
                                       reversed_rotate_position_list[3][1])
        tmp_box.set_position(last_position)
        self.set_box(last_position, tmp_box)
        tmp_box.rotate_color(rotate_mapping)

    def transform(self, direction):
        (axis, axis_position, direction_, rest_axis, edge_position_list, corner_position_list, rotate_mapping) = DirectionToAxis[direction]

        # edge rotate
        self.rotate(axis, axis_position, rest_axis, edge_position_list, rotate_mapping)

        # corner rotate
        self.rotate(axis, axis_position, rest_axis, corner_position_list, rotate_mapping)

        # set feature string
        self.feature = self.calculate_feature()
        self.feature_string = self.calculate_feature_string(self.feature)

    def check(self):
        return self.standard_string == self.feature_string

    def show(self, fp=None):
        def screen_print(bc0, bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8):
            print "%s%s%s%s%s%s%s%s%s" % (bc0, bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8)

        def file_print(bc0, bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8):
            fp.write("%s%s%s%s%s%s%s%s%s\n" % (bc0, bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8))

        show_method = file_print
        if fp is None:
            show_method = screen_print

        # back bottom
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y1, Z3)).get_surface_color(BACK)]
        box_color_4 = COLORS[self.get_box((X2, Y1, Z3)).get_surface_color(BACK)]
        box_color_5 = COLORS[self.get_box((X3, Y1, Z3)).get_surface_color(BACK)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # back middle
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y2, Z3)).get_surface_color(BACK)]
        box_color_4 = COLORS[self.get_box((X2, Y2, Z3)).get_surface_color(BACK)]
        box_color_5 = COLORS[self.get_box((X3, Y2, Z3)).get_surface_color(BACK)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # back top
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y3, Z3)).get_surface_color(BACK)]
        box_color_4 = COLORS[self.get_box((X2, Y3, Z3)).get_surface_color(BACK)]
        box_color_5 = COLORS[self.get_box((X3, Y3, Z3)).get_surface_color(BACK)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # top back
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y3, Z3)).get_surface_color(TOP)]
        box_color_4 = COLORS[self.get_box((X2, Y3, Z3)).get_surface_color(TOP)]
        box_color_5 = COLORS[self.get_box((X3, Y3, Z3)).get_surface_color(TOP)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # top middle
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y3, Z2)).get_surface_color(TOP)]
        box_color_4 = COLORS[self.get_box((X2, Y3, Z2)).get_surface_color(TOP)]
        box_color_5 = COLORS[self.get_box((X3, Y3, Z2)).get_surface_color(TOP)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # top front
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y3, Z1)).get_surface_color(TOP)]
        box_color_4 = COLORS[self.get_box((X2, Y3, Z1)).get_surface_color(TOP)]
        box_color_5 = COLORS[self.get_box((X3, Y3, Z1)).get_surface_color(TOP)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # left front right top
        box_color_0 = COLORS[self.get_box((X1, Y3, Z3)).get_surface_color(LEFT)]
        box_color_1 = COLORS[self.get_box((X1, Y3, Z2)).get_surface_color(LEFT)]
        box_color_2 = COLORS[self.get_box((X1, Y3, Z1)).get_surface_color(LEFT)]
        box_color_3 = COLORS[self.get_box((X1, Y3, Z1)).get_surface_color(FRONT)]
        box_color_4 = COLORS[self.get_box((X2, Y3, Z1)).get_surface_color(FRONT)]
        box_color_5 = COLORS[self.get_box((X3, Y3, Z1)).get_surface_color(FRONT)]
        box_color_6 = COLORS[self.get_box((X3, Y3, Z1)).get_surface_color(RIGHT)]
        box_color_7 = COLORS[self.get_box((X3, Y3, Z2)).get_surface_color(RIGHT)]
        box_color_8 = COLORS[self.get_box((X3, Y3, Z3)).get_surface_color(RIGHT)]
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # left front right middle
        box_color_0 = COLORS[self.get_box((X1, Y2, Z3)).get_surface_color(LEFT)]
        box_color_1 = COLORS[self.get_box((X1, Y2, Z2)).get_surface_color(LEFT)]
        box_color_2 = COLORS[self.get_box((X1, Y2, Z1)).get_surface_color(LEFT)]
        box_color_3 = COLORS[self.get_box((X1, Y2, Z1)).get_surface_color(FRONT)]
        box_color_4 = COLORS[self.get_box((X2, Y2, Z1)).get_surface_color(FRONT)]
        box_color_5 = COLORS[self.get_box((X3, Y2, Z1)).get_surface_color(FRONT)]
        box_color_6 = COLORS[self.get_box((X3, Y2, Z1)).get_surface_color(RIGHT)]
        box_color_7 = COLORS[self.get_box((X3, Y2, Z2)).get_surface_color(RIGHT)]
        box_color_8 = COLORS[self.get_box((X3, Y2, Z3)).get_surface_color(RIGHT)]
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # left front right bottom
        box_color_0 = COLORS[self.get_box((X1, Y1, Z3)).get_surface_color(LEFT)]
        box_color_1 = COLORS[self.get_box((X1, Y1, Z2)).get_surface_color(LEFT)]
        box_color_2 = COLORS[self.get_box((X1, Y1, Z1)).get_surface_color(LEFT)]
        box_color_3 = COLORS[self.get_box((X1, Y1, Z1)).get_surface_color(FRONT)]
        box_color_4 = COLORS[self.get_box((X2, Y1, Z1)).get_surface_color(FRONT)]
        box_color_5 = COLORS[self.get_box((X3, Y1, Z1)).get_surface_color(FRONT)]
        box_color_6 = COLORS[self.get_box((X3, Y1, Z1)).get_surface_color(RIGHT)]
        box_color_7 = COLORS[self.get_box((X3, Y1, Z2)).get_surface_color(RIGHT)]
        box_color_8 = COLORS[self.get_box((X3, Y1, Z3)).get_surface_color(RIGHT)]
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # bottom front
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y1, Z1)).get_surface_color(BOTTOM)]
        box_color_4 = COLORS[self.get_box((X2, Y1, Z1)).get_surface_color(BOTTOM)]
        box_color_5 = COLORS[self.get_box((X3, Y1, Z1)).get_surface_color(BOTTOM)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # bottom middle
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y1, Z2)).get_surface_color(BOTTOM)]
        box_color_4 = COLORS[self.get_box((X2, Y1, Z2)).get_surface_color(BOTTOM)]
        box_color_5 = COLORS[self.get_box((X3, Y1, Z2)).get_surface_color(BOTTOM)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

        # bottom back
        box_color_0 = ' '
        box_color_1 = ' '
        box_color_2 = ' '
        box_color_3 = COLORS[self.get_box((X1, Y1, Z3)).get_surface_color(BOTTOM)]
        box_color_4 = COLORS[self.get_box((X2, Y1, Z3)).get_surface_color(BOTTOM)]
        box_color_5 = COLORS[self.get_box((X3, Y1, Z3)).get_surface_color(BOTTOM)]
        box_color_6 = ' '
        box_color_7 = ' '
        box_color_8 = ' '
        show_method(box_color_0, box_color_1, box_color_2, box_color_3,
                    box_color_4, box_color_5, box_color_6, box_color_7, box_color_8)

    #
    #  9         18            27
	#  8 6       17 15         26 24
	#  7 5 3     16 14 12      25 23 21
	#    4 2        13 11         22 20
	#      1           10            19
    #
    #     FRONT = 0   # WHITE
    #     LEFT = 1    # BLUE
    #     BOTTOM = 2  # ORANGE
    #     BACK = 3    # GREEN
    #     TOP = 4     # RED
    #     RIGHT = 5   # YELLOW
    #
    # eg.
    # WOY BO BOG WO B BG WOB BR BGR WY  O   OG  W       G  WB  R   GR  WYR  OY  OGY  WR  Y   GY  WBR  RY  GRY
    # 1   2  3   4  5 6  7   8  9   10  11  12  13  14  15 16  17  18  19   20  21   22  23  24  25   26  27
    def calculate_feature(self):
        display_list = []
        for x in (X1, X2, X3):
            for y in (Y1, Y2, Y3):
                for z in (Z1, Z2, Z3):
                    box = self.get_box((x, y, z))
                    for surface in range(0, 6):
                        color = box.get_surface_color(surface)
                        if color != NONE:
                            display_list.append(color)
        return display_list

    def calculate_feature_string(self, feature):
        return ''.join([COLORS[color] for color in feature])

    def take_snapshot(self):
        snapshot = [None, None, None, None, None, None]

        # back
        back = dict()
        back[(X1, Y1)] = self.get_box((X1, Y1, Z3)).get_surface_color(BACK)
        back[(X2, Y1)] = self.get_box((X2, Y1, Z3)).get_surface_color(BACK)
        back[(X3, Y1)] = self.get_box((X3, Y1, Z3)).get_surface_color(BACK)
        back[(X1, Y2)] = self.get_box((X1, Y2, Z3)).get_surface_color(BACK)
        back[(X2, Y2)] = self.get_box((X2, Y2, Z3)).get_surface_color(BACK)
        back[(X3, Y2)] = self.get_box((X3, Y2, Z3)).get_surface_color(BACK)
        back[(X1, Y3)] = self.get_box((X1, Y3, Z3)).get_surface_color(BACK)
        back[(X2, Y3)] = self.get_box((X2, Y3, Z3)).get_surface_color(BACK)
        back[(X3, Y3)] = self.get_box((X3, Y3, Z3)).get_surface_color(BACK)
        snapshot[BACK] = back

        # top
        top = dict()
        top[(X1, Z3)] = self.get_box((X1, Y3, Z3)).get_surface_color(TOP)
        top[(X2, Z3)] = self.get_box((X2, Y3, Z3)).get_surface_color(TOP)
        top[(X3, Z3)] = self.get_box((X3, Y3, Z3)).get_surface_color(TOP)
        top[(X1, Z2)] = self.get_box((X1, Y3, Z2)).get_surface_color(TOP)
        top[(X2, Z2)] = self.get_box((X2, Y3, Z2)).get_surface_color(TOP)
        top[(X3, Z2)] = self.get_box((X3, Y3, Z2)).get_surface_color(TOP)
        top[(X1, Z1)] = self.get_box((X1, Y3, Z1)).get_surface_color(TOP)
        top[(X2, Z1)] = self.get_box((X2, Y3, Z1)).get_surface_color(TOP)
        top[(X3, Z1)] = self.get_box((X3, Y3, Z1)).get_surface_color(TOP)
        snapshot[TOP] = top

        # left
        left = dict()
        left[(Y3, Z3)] = self.get_box((X1, Y3, Z3)).get_surface_color(LEFT)
        left[(Y3, Z2)] = self.get_box((X1, Y3, Z2)).get_surface_color(LEFT)
        left[(Y3, Z1)] = self.get_box((X1, Y3, Z1)).get_surface_color(LEFT)
        left[(Y2, Z3)] = self.get_box((X1, Y2, Z3)).get_surface_color(LEFT)
        left[(Y2, Z2)] = self.get_box((X1, Y2, Z2)).get_surface_color(LEFT)
        left[(Y2, Z1)] = self.get_box((X1, Y2, Z1)).get_surface_color(LEFT)
        left[(Y1, Z3)] = self.get_box((X1, Y1, Z3)).get_surface_color(LEFT)
        left[(Y1, Z2)] = self.get_box((X1, Y1, Z2)).get_surface_color(LEFT)
        left[(Y1, Z1)] = self.get_box((X1, Y1, Z1)).get_surface_color(LEFT)
        snapshot[LEFT] = left

        # right
        right = dict()
        right[(Y3, Z1)] = self.get_box((X3, Y3, Z1)).get_surface_color(RIGHT)
        right[(Y3, Z2)] = self.get_box((X3, Y3, Z2)).get_surface_color(RIGHT)
        right[(Y3, Z3)] = self.get_box((X3, Y3, Z3)).get_surface_color(RIGHT)
        right[(Y2, Z1)] = self.get_box((X3, Y2, Z1)).get_surface_color(RIGHT)
        right[(Y2, Z2)] = self.get_box((X3, Y2, Z2)).get_surface_color(RIGHT)
        right[(Y2, Z3)] = self.get_box((X3, Y2, Z3)).get_surface_color(RIGHT)
        right[(Y1, Z1)] = self.get_box((X3, Y1, Z1)).get_surface_color(RIGHT)
        right[(Y1, Z2)] = self.get_box((X3, Y1, Z2)).get_surface_color(RIGHT)
        right[(Y1, Z3)] = self.get_box((X3, Y1, Z3)).get_surface_color(RIGHT)
        snapshot[RIGHT] = right

        # front
        front = dict()
        front[(X1, Y3)] = self.get_box((X1, Y3, Z1)).get_surface_color(FRONT)
        front[(X2, Y3)] = self.get_box((X2, Y3, Z1)).get_surface_color(FRONT)
        front[(X3, Y3)] = self.get_box((X3, Y3, Z1)).get_surface_color(FRONT)
        front[(X1, Y2)] = self.get_box((X1, Y2, Z1)).get_surface_color(FRONT)
        front[(X2, Y2)] = self.get_box((X2, Y2, Z1)).get_surface_color(FRONT)
        front[(X3, Y2)] = self.get_box((X3, Y2, Z1)).get_surface_color(FRONT)
        front[(X1, Y1)] = self.get_box((X1, Y1, Z1)).get_surface_color(FRONT)
        front[(X2, Y1)] = self.get_box((X2, Y1, Z1)).get_surface_color(FRONT)
        front[(X3, Y1)] = self.get_box((X3, Y1, Z1)).get_surface_color(FRONT)
        snapshot[FRONT] = front

        # bottom
        bottom = dict()
        bottom[(X1, Z1)] = self.get_box((X1, Y1, Z1)).get_surface_color(BOTTOM)
        bottom[(X2, Z1)] = self.get_box((X2, Y1, Z1)).get_surface_color(BOTTOM)
        bottom[(X3, Z1)] = self.get_box((X3, Y1, Z1)).get_surface_color(BOTTOM)
        bottom[(X1, Z2)] = self.get_box((X1, Y1, Z2)).get_surface_color(BOTTOM)
        bottom[(X2, Z2)] = self.get_box((X2, Y1, Z2)).get_surface_color(BOTTOM)
        bottom[(X3, Z2)] = self.get_box((X3, Y1, Z2)).get_surface_color(BOTTOM)
        bottom[(X1, Z3)] = self.get_box((X1, Y1, Z3)).get_surface_color(BOTTOM)
        bottom[(X2, Z3)] = self.get_box((X2, Y1, Z3)).get_surface_color(BOTTOM)
        bottom[(X3, Z3)] = self.get_box((X3, Y1, Z3)).get_surface_color(BOTTOM)
        snapshot[BOTTOM] = bottom

        return snapshot


class Sample:
    def __init__(self, feature, direction):
        self.feature = feature
        self.direction = direction

    def normalize_color(self, color):
        return float((float(color) + 1.0) / 6.0)

    def to_direction_vector(self, direction):
        vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if direction > 0:
            vector[direction + 5] = 1.0
        else:
            vector[direction + 6] = 1.0
        return vector

    def to_byte_array_list(self):
        sample_feature_list = [bytearray(struct.pack("f", self.normalize_color(color))) for color in self.feature]
        sample_feature_list.extend([bytearray(struct.pack("f", direction_digit)) for direction_digit in self.to_direction_vector(self.direction)])
        return sample_feature_list


def create_Sample_from_buffer(buff):
    result = []
    for data in buff:
        buf = struct.unpack_from('f', buffer=data)
        result.append(buf[0])
    return result


class Step:
    def __init__(self, sequence_number, direction, previous_step, post_snapshot, feature, feature_string):
        self.sequence_number = sequence_number
        self.direction = direction
        self.previous_step = previous_step
        self.post_snapshot = post_snapshot
        self.feature = feature
        self.feature_string = feature_string

    def print_step(self):
        print self.sequence_number, DIRECTIONS[self.direction + DIRECTION_OFFSET], self.feature_string, \
            self.previous_step.sequence_number if self.previous_step is not None else 'None'


class Game:
    def __init__(self, cube):
        assert isinstance(cube, Cube)
        self.cube = cube
        self.shuffle_full_steps = []
        self.shuffle_steps = []
        self.is_solved = False
        self.solve_steps = []

    def shuffle(self, min_step=64, max_step=1024, directions=None):
        self.shuffle_full_steps = []
        self.shuffle_steps = []
        self.is_solved = False
        self.solve_steps = []

        previous_step = None

        if directions is None:
            real_step = random.randint(min_step, max_step)
            for i in range(0, real_step):
                direction = random.randint(-6, 6)
                while direction == 0:
                    direction = random.randint(-6, 6)
                self.cube.transform(direction)

                step = Step(i, direction, previous_step, self.cube.take_snapshot(), self.cube.feature, self.cube.feature_string)
                self.shuffle_full_steps.append(step)
                step = Step(i, direction, previous_step, self.cube.take_snapshot(), self.cube.feature, self.cube.feature_string)
                self.shuffle_steps.append(step)
                previous_step = step
        else:
            assert isinstance(directions, list)
            i = 0
            for direction in directions:
                self.cube.transform(direction)

                step = Step(i, direction, previous_step, self.cube.take_snapshot(), self.cube.feature, self.cube.feature_string)
                self.shuffle_full_steps.append(step)
                step = Step(i, direction, previous_step, self.cube.take_snapshot(), self.cube.feature, self.cube.feature_string)
                self.shuffle_steps.append(step)
                previous_step = step
                i = i + 1

        self.shuffle_steps = self.eliminate_duplicated_steps()

    def export_to_file_point(self, file_point):
        if file_point is not None:
            for i in range(len(self.shuffle_steps) - 1, -1, -1):
                step = self.shuffle_steps[i]
                sample = Sample(step.feature, step.direction)
                for data in sample.to_byte_array_list():
                    file_point.write(data)
            file_point.flush()

    def export_to_file(self, file_path):
        if file_path is not None:
            with open(file_path, 'w') as fp:
                for i in range(len(self.shuffle_steps) - 1, -1, -1):
                    step = self.shuffle_steps[i]
                    sample = Sample(step.feature, step.direction)
                    for data in sample.to_byte_array_list():
                        fp.write(data)
                fp.flush()

    def eliminate_duplicated_steps(self):
        def sort_duplication_pair_by_length(x, y):
            if x[3] > y[3]: return -1
            if x[3] == y[3]: return 0
            if x[3] < y[3]: return 1

        def sort_duplication_pair_by_start(x, y):
            if x[1] > y[1]: return 1
            if x[1] == y[1]: return 0
            if x[1] < y[1]: return -1

        total_length = len(self.shuffle_steps)
        duplication_pairs = {}
        for step in self.shuffle_steps:
            if step.feature_string in duplication_pairs:
                _, start, _, _ = duplication_pairs[step.feature_string]
                length = step.sequence_number - start
                duplication_pairs[step.feature_string] = (step.feature_string, start, step.sequence_number, length)
            elif step.feature_string == self.cube.standard_string:
                duplication_pairs[step.feature_string] = (step.feature_string, -1, step.sequence_number, step.sequence_number + 1)
            else:
                duplication_pairs[step.feature_string] = (step.feature_string, step.sequence_number, -1, total_length - step.sequence_number - 1)

        def f(s): return s[2] != -1

        ordered = filter(f, [tmp_step for tmp_step in duplication_pairs.itervalues()])
        ordered.sort(cmp=sort_duplication_pair_by_length)

        max_length_idx = 0
        while max_length_idx < len(ordered) - 1:
            max_length_pair = ordered[max_length_idx]
            search_idx = max_length_idx + 1
            while search_idx < len(ordered):
                search_pair = ordered[search_idx]
                if (search_pair[2] > max_length_pair[1] and search_pair[2] <= max_length_pair[2]) or (search_pair[1] >= max_length_pair[1] and search_pair[1] < max_length_pair[2]):
                    ordered.remove(search_pair)
                else:
                    search_idx = search_idx + 1

            max_length_idx = max_length_idx + 1

        ordered.sort(cmp=sort_duplication_pair_by_start)
        for pair in ordered:
            start = pair[1]
            end = pair[2]

            for i in range(start + 1, end + 1):
                self.shuffle_steps[i] = None
            if end + 1 < len(self.shuffle_steps):
                step = self.shuffle_steps[end + 1]
                if start < 0:
                    step.previous_step = None
                else:
                    step.previous_step = self.shuffle_steps[start]

        def f_None(x): return x is not None
        return filter(f_None, self.shuffle_steps)

    def print_shuffle_full_steps(self):
        self.__print_steps__(self.shuffle_full_steps)

    def print_shuffle_steps(self):
        self.__print_steps__(self.shuffle_steps)

    def __print_steps__(self, steps):
        for step in steps:
            step.print_step()

    def play(self, directions):
        for direction in directions:
            self.cube.transform(direction)

    def choose_directon(self):
        return 0

    def solve(self, max_steps=1000):
        self.solve_steps = []
        self.is_solved = False
        step = 0
        direction_str = 'NULL'
        pre_solve_step = None

        while not self.cube.check() or step > max_steps:
            try:
                step = step + 1
                direction = self.choose_directon()
                direction_str = DIRECTIONS[direction + DIRECTION_OFFSET]
                self.cube.transform(direction)
                solve_step = Step(step, direction, pre_solve_step, self.cube.take_snapshot(), self.cube.feature_string)
                self.solve_steps.append(solve_step)
            except RuntimeError as rex:
                print 'Runtime error happens at step %s: %s. Message: %s' % (step, direction_str, rex.message)
                print ''.join([DIRECTIONS[direction + DIRECTION_OFFSET] for direction in self.shuffle_full_steps])

        self.is_solved = self.cube.check()


