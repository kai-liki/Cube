import random

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

# Surface
FRONT = 0   # WHITE
LEFT = 1    # BLUE
BOTTOM = 2  # ORANGE
BACK = 3    # GREEN
TOP = 4     # RED
RIGHT = 5   # YELLOW

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

# Direction axis mapping
DirectionToAxis = {
    # Direction : Axis, Axis position, Direction, (Other 2 axis), [Edge position list], [Corner position list]
    F: (Z, 1, F, (X, Y), [(X1, Y2), (X2, Y3), (X3, Y2), (X2, Y1)], [(X1, Y3), (X3, Y3), (X3, Y1), (X1, Y1)]),
    B: (Z, 3, B, (X, Y), [(X2, Y1), (X3, Y2), (X2, Y3), (X1, Y2)], [(X1, Y1), (X3, Y1), (X3, Y3), (X1, Y3)]),
    L: (X, 1, L, (Y, Z), [(Y2, Z1), (Y1, Z2), (Y2, Z3), (Y3, Z2)], [(Y1, Z1), (Y1, Z3), (Y3, Z3), (Y3, Z1)]),
    R: (X, 3, R, (Y, Z), [(Y2, Z1), (Y3, Z2), (Y2, Z3), (Y1, Z2)], [(Y1, Z1), (Y3, Z1), (Y3, Z3), (Y1, Z3)]),
    D: (Y, 1, D, (X, Z), [(X2, Z1), (X3, Z2), (X2, Z3), (X1, Z2)], [(X1, Z1), (X3, Z1), (X3, Z3), (X1, Z3)]),
    U: (Y, 3, U, (X, Z), [(X2, Z1), (X1, Z2), (X2, Z3), (X3, Z2)], [(X1, Z1), (X1, Z3), (X3, Z3), (X3, Z1)]),
    F_: (Z, 1, F_, (X, Y), [(X2, Y1), (X3, Y2), (X2, Y3), (X1, Y2)], [(X1, Y1), (X3, Y1), (X3, Y3), (X1, Y3)]),
    R_: (X, 3, R_, (Y, Z), [(Y2, Z1), (Y1, Z2), (Y2, Z3), (Y3, Z2)], [(Y1, Z1), (Y1, Z3), (Y3, Z3), (Y3, Z1)]),
    B_: (Z, 3, B_, (X, Y), [(X1, Y2), (X2, Y3), (X3, Y2), (X2, Y1)], [(X1, Y3), (X3, Y3), (X3, Y1), (X1, Y1)]),
    L_: (X, 1, L_, (Y, Z), [(Y2, Z1), (Y3, Z2), (Y2, Z3), (Y1, Z2)], [(Y1, Z1), (Y3, Z1), (Y3, Z3), (Y1, Z3)]),
    D_: (Y, 1, D_, (X, Z), [(X2, Z1), (X1, Z2), (X2, Z3), (X3, Z2)], [(X1, Z1), (X1, Z3), (X3, Z3), (X3, Z1)]),
    U_: (Y, 3, U_, (X, Z), [(X2, Z1), (X3, Z2), (X2, Z3), (X1, Z2)], [(X1, Z1), (X3, Z1), (X3, Z3), (X1, Z3)]),
}

EDGE_ROTATE_XY = {
    (X1, Y2): (Y2, X1),
    (X2, Y1): (X3, Y2),
    (X3, Y2): (X2, Y3),
    (X2, Y3): (X1, Y2)
}

EDGE_ROTATE_YX = {
    (X2, Y1): (X1, Y2),
    (X3, Y2): (X2, Y1),
    (X2, Y3): (X3, Y2),
    (X1, Y2): (X2, Y3)
}

EDGE_ROTATE_YZ = {
    (Y1, Z2): (Y2, Z1),
    (Y2, Z1): (Y3, Z2),
    (Y3, Z2): (Y2, Z3),
    (Y2, Z3): (Y1, Z2)
}

EDGE_ROTATE_ZY = {
    (Y2, Z1): (Y1, Z2),
    (Y3, Z2): (Y2, Z1),
    (Y2, Z3): (Y3, Z2),
    (Y1, Z2): (Y2, Z3)
}

EDGE_ROTATE_XZ = {
    (X1, Z2): (X2, Z1),
    (X2, Z1): (X3, Z2),
    (X3, Z2): (X2, Z3),
    (X2, Z3): (X1, Z2)
}

EDGE_ROTATE_ZX = {
    (X2, Z1): (X1, Z2),
    (X3, Z2): (X2, Z1),
    (X2, Z3): (X3, Z2),
    (X1, Z2): (X2, Z3)
}


def build_box(position, colors):
    count_2 = 0
    for i in position:
        if i == 2:
            count_2 = count_2 + 1
    if count_2 == 0:
        return CenterBox(position, CORNER, colors)
    elif count_2 == 1:
        return CenterBox(position, EDGE, colors)
    else:
        return CenterBox(position, CENTER, colors)


class Box:
    def __init__(self, position, position_type, colors):
        self.position = position
        self.colors = colors
        self.type = position_type

    def get_surface_color(self, surface):
        return self.colors[surface]

    def transform(self, direction, cube):
        pass

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


class CenterBox(Box):
    def transform(self, direction, cube):
        self.validate_transform(direction)
        pass


class EdgeBox(Box):
    def transform(self, direction, cube):
        self.validate_transform(direction)
        pass


class CornerBox(Box):
    def transform(self, direction, cube):
        self.validate_transform(direction)
        pass


class Cube:
    COLORS = ('R', 'Y', 'B', 'G', 'O', 'W')

    def __init__(self):
        self.boxes = self.construct_standard()

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

    def transform(self, direction):
        (axis, axis_position, direction_, rest_axis, edge_position_list, corner_position_list) = DirectionToAxis[direction]

