from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_
from difflib import unified_diff
from sys import stdout

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


def test_transform():
    result_file = 'tmp_result.txt'
    benchmark_file = 'ut_result.txt'
    cube = Cube()
    with open(result_file, 'w') as result_fp:
        cube.show(result_fp)
        for command in command_list:
            for i in range(0, 4):
                result_fp.write('=========== %s ============\n' % command)
                cube.transform(command_list[command])
                cube.show(result_fp)

    benchmark = open(result_file, 'U').readlines()
    result = open(benchmark_file, 'U').readlines()

    diff = unified_diff(benchmark, result, benchmark_file, result_file)

    print 'Diff between benchmark and result.\n'
    stdout.writelines(diff)
    print '\nTest transform done.'


def main():
    test_transform()
    print 'Done'


if __name__ == '__main__':
    main()
