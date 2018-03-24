from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_

command_list = [
    F,
    B,
    R,
    L,
    U,
    D,
    F_,
    B_,
    R_,
    L_,
    U_,
    D_,
]


def main():
    cube = Cube()
    with open('tmp_result.txt', 'w') as result_fp:
        cube.show(result_fp)
        for command in command_list:
            for i in range(0, 4):
                result_fp.write('=========== %s ============\n' % command)
                cube.transform(command_list[command])
                cube.show(result_fp)


if __name__ == '__main__':
    main()
