from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_
from cube.model import Game
from cube.model import create_Sample_from_buffer
from cube.model import DIRECTIONS, DIRECTION_OFFSET

command_map = {
    'F': F,
    'B': B,
    'R': R,
    'L': L,
    'U': U,
    'D': D,
    'F-': F_,
    'B-': B_,
    'R-': R_,
    'L-': L_,
    'U-': U_,
    'D-': D_,
}


def test_shuffle():
    cube = Cube()
    game = Game(cube)
    game.shuffle()
    step = len(game.shuffle_full_steps)
    print '=========== initialized with %s-step shuffle ============' % step
    cube.show()
    print ''
    print 'Feature string is ', cube.calculate_feature_string()
    print 'Is standard? ', cube.check()
    command = raw_input("Command: ").upper()
    while command != 'Q':
        if command not in command_map:
            print("Invalid input. Input again.")
            continue
        cube.transform(command_map[command])
        print '=========== %s ============' % command
        print ''
        cube.show()
        print ''
        command = raw_input("Command: ").upper()


def test_shuffle_elimination(directions):
    cube = Cube()
    game = Game(cube)
    game.shuffle(directions=directions)
    print '============= FULL STEPS =============='
    game.print_shuffle_full_steps()
    print '============= ELIMINATED STEPS =============='
    game.print_shuffle_steps()


def validate_shuffle_elimination():
    cube = Cube()
    game = Game(cube)
    game.shuffle()
    # print '============= FULL STEPS =============='
    # game.print_shuffle_full_steps()
    # print '============= ELIMINATED STEPS =============='
    # game.print_shuffle_steps()
    print 'Full steps: ', len(game.shuffle_full_steps)
    print 'Steps: ', len(game.shuffle_steps)
    directions = [-step.direction for step in game.shuffle_steps]
    directions.reverse()
    # print [DIRECTIONS[direction + DIRECTION_OFFSET] for direction in directions]
    game.play(directions)
    assert game.cube.check()
    print 'Validation PASS!'
    return True


def main():
    # test_shuffle()
    # test_shuffle_elimination(directions=[F, L, L, L, L, F])
    # test_shuffle_elimination(directions=[F, L, L, L, L])
    # test_shuffle_elimination(directions=[L, L, L, L])
    # test_shuffle_elimination(directions=[L, L, L, L, F])
    # test_shuffle_elimination(directions=[F, B, L, L, L, L, L, R])
    # test_shuffle_elimination(directions=[F, B, L, L_, B_])

    # for i in range(0, 100000):
    #     print i
    #     validate_shuffle_elimination()

    cube = Cube()
    game = Game(cube)
    game.shuffle(min_step=3, max_step=3, sample_file='./sample_file.dat')
    print 'Full step'
    game.print_shuffle_full_steps()
    print 'Step'
    game.print_shuffle_steps()

    with open('./sample_file.dat', 'r') as fp:
        is_eof = False
        while True:
            step_sample = []
            for i in range(0, 55):
                data = fp.read(4)
                if '' == data:
                    is_eof = True
                else:
                    step_sample.append(data)
            print create_Sample_from_buffer(step_sample)
            if is_eof:
                break


if __name__ == '__main__':
    main()
