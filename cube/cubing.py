from model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_, DIRECTIONS, DIRECTION_OFFSET


HISTORY_STEPS = []
ITER_DIRECTIONS = [F, B, R, L, U, D, F_, B_, R_, L_, U_, D_]
FEATURE_STRING_SET = set()


def on_success(direction=None):
    if direction is not None:
        HISTORY_STEPS.append(direction)
    print "Success!\nDepth: %s \n %s" % \
          (len(HISTORY_STEPS), ''.join([DIRECTIONS[direction + DIRECTION_OFFSET] for direction in HISTORY_STEPS]))


def on_error(message):
    print message
    print ''.join([DIRECTIONS[direction + DIRECTION_OFFSET] for direction in HISTORY_STEPS])
    print len(FEATURE_STRING_SET)


def find_feature_string(feature_string):
    return feature_string in FEATURE_STRING_SET


def turn_one(cube, direction):
    assert isinstance(cube, Cube)
    cube.transform(direction)
    if cube.check():
        on_success(direction)
        return True

    # Found loop
    if find_feature_string(cube.feature_string):
        cube.transform(-direction)
        return False

    FEATURE_STRING_SET.add(cube.feature_string)
    HISTORY_STEPS.append(direction)
    for next_direction in ITER_DIRECTIONS:
        if next_direction == -direction:
            continue
        if turn_one(cube, next_direction):
            return True
    # FEATURE_STRING_SET.remove(cube.feature_string)
    HISTORY_STEPS.pop()


def turn(cube):
    assert isinstance(cube, Cube)
    if cube.check():
        on_success()
        return True
    try:
        FEATURE_STRING_SET.add(cube.feature_string)
        for next_direction in ITER_DIRECTIONS:
            if turn_one(cube, next_direction):
                return True
    except RuntimeError as rex:
        on_error(rex.message)
    return False

