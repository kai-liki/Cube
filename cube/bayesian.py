import yaml


total_times = 0
features = {}
decisions = {}


class Feature:
    def __init__(self, feature_str):
        self.feature_str = feature_str
        self.appear_times = 0


class Decision:
    def __init__(self, name):
        self.name = name
        self.appear_times = 0
        # key: feature_str
        # value: appear_times with this decision
        self.features = {}


def add_feature_and_decision(feature_str, decision_name):
    if feature_str in features:
        feature = features[feature_str]
    else:
        feature = Feature(feature_str)
        features[feature_str] = feature

    if decision_name in decisions:
        decision = decisions[decision_name]
    else:
        decision = Decision(decision_name)
        decisions[decision_name] = decision

    feature.appear_times = feature.appear_times + 1
    decision.appear_times = decision.appear_times + 1

    global total_times
    total_times = total_times + 1

    if feature_str not in decision.features:
        decision.features[feature_str] = 1
    else:
        decision.features[feature_str] = decision.features[feature_str] + 1


def possibility_decision(decision_name):
    global total_times
    if total_times == 0:
        return 0.0
    if decision_name not in decisions:
        return 0.0
    decision = decisions[decision_name]
    return float(float(decision.appear_times) / float(total_times))


def possibility_feature(feature_str):
    global total_times
    if total_times == 0:
        return 0.0
    if feature_str not in features:
        return 0.0
    feature = features[feature_str]
    return float(float(feature.appear_times) / float(total_times))


def possibility_decision_feature(decision_name, feature_str):
    if decision_name not in decisions:
        return 0.0
    decision = decisions[decision_name]
    if feature_str not in decision.features:
        return 0.0

    return float(float(decision.features[feature_str]) / float(decision.appear_times))


def export(file_path):
    global total_times
    result = {'total_times': total_times, 'features': features, 'decisions': decisions}

    with open(file_path, 'w') as fp:
        yaml.dump(result, fp)


def load(file_path):
    global total_times, features, decisions
    root_json = None
    with open(file_path, 'r') as fp:
        root_json = yaml.load(fp)

    assert isinstance(root_json, dict)
    total_times = root_json['total_times']
    features = root_json['features']
    decisions = root_json['decisions']
