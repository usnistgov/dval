"""
All metrics used in the D3M Program, mapped to their function.
>>> from d3m_outputs.metrics import apply_metric
>>> groundtruth_file = 'test/data/185_baseball_SCORE/targets.csv'
>>> predictions_file = 'test/data/185_baseball_SCORE/mitll_predictions.csv'

>>> apply_metric('rootMeanSquaredError', groundtruth_file, predictions_file)
0.42
"""

import numpy as np
import sklearn.metrics as skm
from sklearn.preprocessing import LabelBinarizer

from d3m_outputs.object_detection_ap import objectDetectionAP


def accuracy(ground_truth, predicted):
    return skm.accuracy_score(ground_truth, predicted)


def f1(ground_truth, predicted, pos_label=1):
    # if pos_label:
    #     return skm.f1_score(ground_truth, predicted, pos_label=pos_label)
    return skm.f1_score(ground_truth, predicted, pos_label=pos_label)


def f1_micro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average='micro')


def f1_macro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average='macro')


def roc_auc(ground_truth, predicted, pos_label=None):
    if pos_label is not None:
        ground_truth, predicted = _binarize(ground_truth, predicted, pos_label)
    return skm.roc_auc_score(ground_truth, predicted)


def roc_auc_micro(ground_truth, predicted):
    ground_truth, predicted = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average='micro')


def roc_auc_macro(ground_truth, predicted):
    ground_truth, predicted = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average='macro')


def l2(ground_truth, predicted):
    return skm.mean_squared_error(ground_truth, predicted) ** 0.5


def avg_l2(ground_truth_l, predicted_l):
    '''
    This function takes a list of ground truth vectors and a list
    of predicted vectors and calculates the average L2 metrics between
    them.

    The vectors are transposed because the skm.mse(multioutputs='raw_values')
    Will compute the following:

        >>> import sklearn.metrics as skm
        
        >>> y_true = [[0.5, 1],[-1, 1],[7, -6]]
        >>> y_pred = [[0, 2],[-1, 2],[8, -5]]

        >>> skm.mean_squared_error(y_true, y_pred, multioutput='raw_values')
        array([0.41666667, 1.        ])

    Parameters:
    -----------
    ground_truth_l: list
     List of ground truth vectors having the following shape:
        [[X1, Y1], ... , [Xn, Yn, ...]]

    predicted_l: list
     List of predicted vectors having the following shape:
        [[x1, y1], ... , [xn, yn, ...]]

    Returns:
    --------
    
    avg_l2:
     avg(sqrt(mse(X,x)), sqrt(mse(Y,y)) )

    '''

    return np.mean(skm.mean_squared_error(ground_truth_l, predicted_l, multioutput='raw_values') ** 0.5)


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

    if pos_label is not None and lb.classes_[0] == pos_label:
        return 1 - binary_ground, 1 - binary_pred
    else:
        return binary_ground, binary_pred


def precision_at_top_K_meta(gt, preds, K=20):
    def precision_at_top_K(gt, preds, K):
        """
        This function examines the first K entries of a
        ground truth vector (gt) and predicted labels (preds)
        and determines how many values are shared between them.
        The result is then scaled by K to get the accuracy at top K.

        Parameters:
        -----------
        gt: 1d array-like
            Array of ground truth labels.

        preds: 1d array-like
            Array of predicted labels.

        K: int, 20 by default
            The number of samples to use when computing the accuracy.

        Returns:
        --------
        prec_at_top_K: float
            The number of labels shared between the ground truth and
            the predictions divided by K.


        Example:
            >>> gt = [0, 1, 2, 3, 4]
            >>> pred = [1, 3, 2, 4, 0]

            >>> precision_at_top_K(gt, pred, K=3)
            0.667

            >>> precision_at_top_K(gt, pred, K=4)
            0.75
        """

        gt = gt[0:K]
        preds = preds[0:K]
        prec_at_top_K = np.float(len(np.intersect1d(gt, preds))) / K
        return prec_at_top_K

    # sort preds indice
    pred_indices = np.argsort(preds)[::-1]
    # sort gt indices
    gt_indices = np.argsort(gt)[::-1]

    return precision_at_top_K(gt_indices, pred_indices, K=K)


def precision(ground_truth, predicted):
    return skm.precision_score(ground_truth, predicted)


def recall(ground_truth, predicted):
    return skm.recall_score(ground_truth, predicted)

def log_loss(ground_truth, predicted):
    return skm.log_loss(ground_truth, predicted)

mxe = log_loss

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
    'jaccardSimilarityScore': jacc_sim,
    'precisionAtTopK': precision_at_top_K_meta,
    'objectDetectionAP': objectDetectionAP,
    'object_detection_average_precision': objectDetectionAP,
    'precision': precision,
    'recall': recall,
    'crossEntropy': mxe
}

def find_metric(metric, valid_metrics=METRICS_DICT):
    def transform_string(string):
        return string.lower().replace('_', '')

    reference = {transform_string(k): _ for k,_ in valid_metrics.items()}
    return reference[transform_string(metric)]


def valid_metric(metric):
    try:
        _ = find_metric(metric)
    except KeyError:
        return False
    return True


def apply_metric(metric, *args, **kwargs):
    return find_metric(metric)(*args, **kwargs)
