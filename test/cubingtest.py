from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_
from cube.model import Game, DIRECTIONS, DIRECTION_OFFSET
import cube.cubing
import os.path
import sys


def generate_file(file_path, data_num, min_step, max_step):
    with open(file_path, 'w') as fp:
        for i in range(0, data_num):
            c = Cube()
            game = Game(c)
            game.shuffle(min_step=min_step, max_step=max_step)
            game.export_to_file_point(fp)
            print '%s generate %i' % (file_path, i)


def test_train_and_test():
    sample_file_path = './sample_file.dat'
    if not os.path.exists(sample_file_path):
        generate_file(sample_file_path, 100000, 10, 1024)

    test_file_path = './test_file.dat'
    if not os.path.exists(test_file_path):
        generate_file(test_file_path, 1000, 10, 100)

    cube.cubing.train_and_test(sample_data_file=sample_file_path, test_data_file=test_file_path)


def test_train_and_solve():
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


def main():
    test_train_and_test()

if __name__ == '__main__':
    main()
