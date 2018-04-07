from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_
from cube.model import Game, DIRECTIONS, DIRECTION_OFFSET
import sys


print sys.getrecursionlimit()
sys.setrecursionlimit(5000)


def main():
    cube = Cube()
    game = Game(cube)
    game.shuffle()
    step = len(game.shuffle_full_steps)
    print '=========== initialized with %s-step shuffle ============' % step
    cube.show()
    print 'Solving . . . . . . '
    game.solve()
    cube.show()
    if game.is_solved:
        print 'Congratulations!!!! Solved after %s steps!' % len(game.solve_steps)
        print ('Steps: %s' % ''.join([DIRECTIONS[step.direction + DIRECTION_OFFSET] for step in game.solve_steps]))
    else:
        print 'Stupid!!!! Cannot solve a cube in %s steps!' % len(game.solve_steps)


if __name__ == '__main__':
    main()
