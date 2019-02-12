"""
All metrics used in the D3M Program, mapped to their function.
>>> from d3m_outputs.metrics import apply_metric
>>> groundtruth_file = 'test/data/185_baseball_SCORE/targets.csv'
>>> predictions_file = 'test/data/185_baseball_SCORE/mitll_predictions.csv'

>>> apply_metric('rootMeanSquaredError', groundtruth_file, predictions_file)
0.42
"""

import math
from collections import defaultdict

import numpy as np
import sklearn.metrics as skm
from sklearn.preprocessing import LabelBinarizer

from d3m_outputs.object_detection_ap import objectDetectionAP


def accuracy(ground_truth, predicted):
    return skm.accuracy_score(ground_truth, predicted)


def f1(ground_truth, predicted, pos_label=1):
    return skm.f1_score(ground_truth, predicted, pos_label=pos_label)


def f1_micro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average="micro")


def f1_macro(ground_truth, predicted):
    return skm.f1_score(ground_truth, predicted, average="macro")


def roc_auc(ground_truth, predicted, pos_label=None):
    if pos_label is not None:
        ground_truth, predicted, _ = _binarize(ground_truth, predicted, pos_label)
    return skm.roc_auc_score(ground_truth, predicted)


def roc_auc_micro(ground_truth, predicted):
    ground_truth, predicted, _ = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average="micro")


def roc_auc_macro(ground_truth, predicted):
    ground_truth, predicted, _ = _binarize(ground_truth, predicted)
    return skm.roc_auc_score(ground_truth, predicted, average="macro")


def l2(ground_truth, predicted):
    return skm.mean_squared_error(ground_truth, predicted) ** 0.5


def avg_l2(ground_truth_l, predicted_l):
    """
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

    """

    return np.mean(
        skm.mean_squared_error(ground_truth_l, predicted_l, multioutput="raw_values")
        ** 0.5
    )


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
    """
    Binarize a prediction according to the classes
    available in the ground truth

    Parameters:
    -----------
    ground: 1d array
        Array of ground truth labels.

    pred: 1d array
        Array of predicted labels.

    Returns:
    --------
    (binary_ground, binary_pred, classes): tuples
        Tuple composed of binarized ground truth, binarized predictions and associated classes.

    Example:
        >>> ground = [0, 1, 2, 1]
        >>> pred = [0, 0, 2, 1]

        binary_ground = [[1,0,0], [0,1,0], [0,0,1], [0,1,0]]
        binary_pred = [[1,0,0], [1,0,0], [0,0,1], [0,1,0]]
        classes = [0, 1, 2]
    """
    lb = LabelBinarizer()
    binary_ground = lb.fit_transform(ground)
    classes = lb.classes_
    binary_pred = lb.transform(pred)

    if pos_label is not None and lb.classes_[0] == pos_label:
        return 1 - binary_ground, 1 - binary_pred, classes
    else:
        return binary_ground, binary_pred, classes


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


def mxe_non_bin(ground_truth, predicted):
    """
    This function converts non-binarized predicted values
    and pass them to the crossEntropy function


    Parameters:
    -----------
    ground_truth: array
        Array of non-binarized vectors.

    predicted: array
        Array of non-binarized predicted vectors.

    Returns:
    --------
    cross_entropy:
        Cross entropy of the predicted values


    Example:
        >>> ground_truth = [0, 1, 2, 2, 1]
        >>> predicted = [0, 1, 2, 1, 0]

        bin_predicted = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1], [0, 1, 0]]
        classes = [0, 1, 2]
    """
    _, bin_predicted, classes = _binarize(ground_truth, predicted)
    return apply_metric("crossEntropy", ground_truth, bin_predicted, classes)


def _normalize_ground_truth(ground_truth, classes):
    """
    Convert the ground truth list into a list of classe indices.
    First it transforms the list of classes into a dictionary where
    the key is the class name and the value is its indice in the list.
    The order of the classes in the list is mapped to the order of the
    confidence factors in the predictions.
    Then, it replace every class value in the ground truth by its indice.

    Parameters:
    -----------
    ground_truth: 1d array
        Array of ground truth.

    classes: 1d array
        Array of the classes available in the ground truth.

    Return:
    -------
    ground_truth_normalized: array
        Array of class indices.

    Example:
        >>> ground_truth = ['val_a', 'val_c', 'val_b', 'val_c']
        >>> classes = ['val_a', 'val_b', 'val_c']

        ground_truth_classes = {'val_a': 0, 'val_b': 1, 'val_c': 2}
        ground_truth_normalized = [0, 2, 1, 2]
    """
    # Build dictionary based on ground_truth classes order
    i = 0
    ground_truth_classes = {}
    for gt_class in classes:
        ground_truth_classes[gt_class] = i
        i += 1

    # Process the ground truth
    ground_truth_normalized = []
    for value in ground_truth:
        ground_truth_normalized.append(ground_truth_classes[value])
    return ground_truth_normalized


def _normalize_predicted(predicted, eps_value=2 ** -100):
    norm_predicted = []
    for trial in predicted:
        t = []
        for pd in trial:
            # Here, we convert any value less than eps_value to eps_value
            if pd == 0 or (pd < eps_value):
                pd = eps_value
            t.append(math.log(pd))
        norm_predicted.append(t)
    return norm_predicted


def mxe(ground_truth, predicted, classes):
    """
    Computes the Multiclass Cross Entropy (MXE).

    Parameters:
    -----------
    ground_truth: 1d array
        Array of ground truth

    predicted: 1d array
        Array of predictions

    classes: 1d array
        Array of classes composing the ground truth. The order of the class values
        defines the order of prediction values.

    Return:
    -------
        mxe_score
    """
    log_base = 2
    ground_truth = _normalize_ground_truth(ground_truth, classes)
    predicted = _normalize_predicted(predicted)
    class_to_trials = defaultdict(list)
    for gt, pd in zip(ground_truth, predicted):
        class_to_trials[gt].append(pd)
    numerator = 0
    for gt_cls, trials in class_to_trials.items():
        class_loss = sum(
            [
                math.log(
                    sum([math.e ** (pd) for pd in trial]) / math.e ** (trial[gt_cls]),
                    log_base,
                )
                for trial in trials
            ]
        )
        numerator += class_loss / len(trials)
    num_classes = len(class_to_trials)
    return numerator / num_classes


METRICS_DICT = {
    "accuracy": accuracy,
    "f1": f1,
    "f1Micro": f1_micro,
    "f1Macro": f1_macro,
    "rocAuc": roc_auc,
    "rocAucMicro": roc_auc_micro,
    "rocAucMacro": roc_auc_macro,
    "meanSquaredError": mean_se,
    "rootMeanSquaredError": l2,
    "rootMeanSquaredErrorAvg": avg_l2,
    "meanAbsoluteError": l1,
    "rSquared": r2,
    "normalizedMutualInformation": norm_mut_info,
    "jaccardSimilarityScore": jacc_sim,
    "precisionAtTopK": precision_at_top_K_meta,
    "objectDetectionAP": objectDetectionAP,
    "object_detection_average_precision": objectDetectionAP,
    "precision": precision,
    "recall": recall,
    "crossEntropy": mxe,
    "crossEntropyNonBinarized": mxe_non_bin,
}


def find_metric(metric, valid_metrics=METRICS_DICT):
    def transform_string(string):
        return string.lower().replace("_", "")

    reference = {transform_string(k): _ for k, _ in valid_metrics.items()}
    return reference[transform_string(metric)]


def valid_metric(metric):
    try:
        _ = find_metric(metric)
    except KeyError:
        return False
    return True


def apply_metric(metric, *args, **kwargs):
    return find_metric(metric)(*args, **kwargs)
