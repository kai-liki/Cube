from cube.model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_
from cube.model import DIRECTIONS, DIRECTION_OFFSET
from cube.model import Game
import cube.bayesian as bayesian


def print_possibility():
    direction_list = [F, B, R, L, U, D, F_, B_, R_, L_, U_, D_]
    feature_set = set()
    for direction in direction_list:
        decision_name = DIRECTIONS[direction + DIRECTION_OFFSET]
        print "===", decision_name, bayesian.possibility_decision(decision_name)

        if decision_name in bayesian.decisions:
            decision = bayesian.decisions[decision_name]
            for feature_str in dict.iterkeys(decision.features):
                print feature_str, bayesian.possibility_decision_feature(decision_name, feature_str)
                feature_set.add(feature_str)

    print "================ Features ================"
    for feature_str in feature_set:
        print feature_str, bayesian.possibility_feature(feature_str)


def test_bayesian():
    cube = Cube()

    cube.transform(F)
    bayesian.add_feature_and_decision(cube.feature_string, DIRECTIONS[-F + DIRECTION_OFFSET])

    cube.transform(B)
    bayesian.add_feature_and_decision(cube.feature_string, DIRECTIONS[-B + DIRECTION_OFFSET])

    print_possibility()


def main():
    test_bayesian()


if __name__ == '__main__':
    main()
