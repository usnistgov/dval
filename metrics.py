"""
All metrics used in the D3M Program, mapped to their function.

>>> from metrics import apply_metric
>>> apply_metric('rootMeanSquaredError', ground_truth, predicted)
0.42
"""

import sklearn.metrics as skm
from sklearn.preprocessing import LabelBinarizer


def accuracy(ground_truth, predicted):
    return skm.accuracy_score(ground_truth, predicted)


def f1(ground_truth, predicted, pos_label=None):
    if pos_label:
        return skm.f1_score(ground_truth, predicted, pos_label=pos_label)
    return skm.f1_score(ground_truth, predicted)


def f1_micro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average='micro')


def f1_macro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average='macro')


def roc_auc(ground_truth, predicted, pos_label=None):
    if pos_label:
        ground_truth, predicted = _binarize(ground_truth, predicted, pos_label)
    return skm.roc_auc_score(ground_truth, predicted)


def roc_auc_micro(ground_truth, predicted):
    ground_truth, predicted = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average='micro')


def roc_auc_macro(ground_truth, predicted):
    ground_truth, predicted = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average='macro')


def l2(ground_truth, predicted):
    return (skm.mean_squared_error(ground_truth, predicted)) ** 0.5


def avg_l2(ground_truth_l, predicted_l):
    l2_sum = 0.0
    count = 0
    for pair in zip(ground_truth_l, predicted_l):
        l2_sum += l2(pair[0], pair[1])
        count += 1
    return l2_sum / count


def mean_se(ground_truth, predicted):
    return skm.mean_squared_error(ground_truth, predicted)


def l1(ground_truth, predicted):
    return skm.mean_absolute_error(ground_truth, predicted)


def r2(ground_truth, predicted):
    return skm.r2_score(ground_truth, predicted)


def norm_mut_info(ground_truth, predicted):
    return skm.normalized_mutual_info_score(ground_truth, predicted)


def jacc_sim(ground_truth, predicted):
    return skm.jaccard_similarity_score(ground_truth, predicted)


def _binarize(ground, pred, pos_label=None):
    lb = LabelBinarizer()
    binary_ground = lb.fit_transform(ground)
    binary_pred = lb.transform(pred)

    if pos_label and lb.classes_[0] == pos_label:
        return 1 - binary_ground, 1 - binary_pred
    else:
        return binary_ground, binary_pred


def valid_metric(metric):
    return metric in METRICS_DICT


def apply_metric(metric, *args, **kwargs):
    return METRICS_DICT[metric](*args, **kwargs)


METRICS_DICT = {
    'accuracy': accuracy,
    'f1': f1,
    'f1Micro': f1_micro,
    'f1Macro': f1_macro,
    'rocAuc': roc_auc,
    'rocAucMicro': roc_auc_micro,
    'rocAucMacro': roc_auc_macro,
    'meanSquaredError': mean_se,
    'rootMeanSquaredError': l2,
    'rootMeanSquaredErrorAvg': avg_l2,
    'meanAbsoluteError': l1,
    'rSquared': r2,
    'normalizedMutualInformation': norm_mut_info,
    'jaccardSimilarityScore': jacc_sim
}
