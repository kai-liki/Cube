from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_

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


def main():
    cube = Cube()
    print '=========== initial ============'
    cube.show()
    print cube.calculate_feature_string()
    print cube.check()
    print ''
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


if __name__ == '__main__':
    main()
