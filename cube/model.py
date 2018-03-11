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

EDGE_ROTATE_XY = {
    (X1, Y2):(Y2, X1),
    (X2, Y1):(X3, Y2),
    (X3, Y2):(X2, Y3),
    (X2, Y3):(X1, Y2)
}

EDGE_ROTATE_YX = {
    (X2, Y1):(X1, Y2),
    (X3, Y2):(X2, Y1),
    (X2, Y3):(X3, Y2),
    (X1, Y2):(X2, Y3)
}

EDGE_ROTATE_YZ = {
    (Y1, Z2):(Y2, Z1),
    (Y2, Z1):(Y3, Z2),
    (Y3, Z2):(Y2, Z3),
    (Y2, Z3):(Y1, Z2)
}

EDGE_ROTATE_ZY = {
    (Y2, Z1):(Y1, Z2),
    (Y3, Z2):(Y2, Z1),
    (Y2, Z3):(Y3, Z2),
    (Y1, Z2):(Y2, Z3)
}

EDGE_ROTATE_XZ = {
    (Y1, Z2):(Y2, Z1),
    (Y2, Z1):(Y3, Z2),
    (Y3, Z2):(Y2, Z3),
    (Y2, Z3):(Y1, Z2)
}

EDGE_ROTATE_ZX = {
    (Y2, Z1):(Y1, Z2),
    (Y3, Z2):(Y2, Z1),
    (Y2, Z3):(Y3, Z2),
    (Y1, Z2):(Y2, Z3)
}




class Box:
    def __init__(self, position, colors):
        self.position = position
        self.colors = colors
        count_2 = 0
        for i in position:
            if i == 2:
                count_2 = count_2 + 1
        if count_2 == 0:
            self.type = CORNER
        elif count_2 == 1:
            self.type = EDGE
        else:
            self.type = CENTER

    def get_surface_color(self, surface):
        return self.colors[surface]

    def transform(self, direction):
        if self.type == CENTER:
            self.transform_center(direction)
        elif self.type == EDGE:
            self.transform_edge(direction)
        elif self.type == CORNER:
            self.transform_corner(direction)

    def transform_center(self, direction):
        self.validate_transform(direction)
        pass

    def transform_edge(self, direction):
        self.validate_transform(direction)
        if direction in (L, R_):

            pass
        elif direction in (L_, R):
            pass
        pass

    def transform_corner(self, direction):
        self.validate_transform(direction)
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

    def rotate_edge_XY(self, x, y):
        pass

class Cube:
    COLORS = ('R', 'Y', 'B', 'G', 'O', 'W')

    def __init__(self):
        pass