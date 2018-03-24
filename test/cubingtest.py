from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_
from cube.cubing import turn
import sys


print sys.getrecursionlimit()
sys.setrecursionlimit(5000)


def main():
    cube = Cube()
    step = cube.shuffle()
    print '=========== initialized with %s-step shuffle ============' % step
    cube.show()
    print ''
    turn(cube)
    cube.show()


if __name__ == '__main__':
    main()
