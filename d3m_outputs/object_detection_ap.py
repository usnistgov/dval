import logging

import numpy as np


def group_gt_boxes_by_image_name(gt_boxes):
    """
    This function takes a list of ground truth boxes and turn them into a
    dict mapping an image name to an array containing the 4 coordinates of
    the edges delimiting a bounding box

    Parameters:
    -----------
    gt_boxes: list
     List of ground truth boxes. Each box is represented as a list with the
     following format: [image_name, x_min, y_min, x_max, y_max].

    Returns:
    --------
    gt_dict: dict
     Dictionary mapping every image name to an array of the bounding boxes:
        {'image_name' : [
                {'bbox': [x_min, y_min, x_max, y_max]},
                {'bbox': [x_min, y_min, x_max, y_max]},
                ...
            ]
        }

    """
    gt_dict = {}

    for box in gt_boxes:

        image_name = box[0]
        bbox = box[1:]

        if image_name not in gt_dict.keys():
            gt_dict[image_name] = []

        gt_dict[image_name].append({"bbox": bbox})

    return gt_dict


def unvectorize(targets):
    """
    If ``targets`` have two columns (index, object detection target) or three (index, object detection
    target, confidence), we make it into 5 or 6, respectively, by splitting the second column into
    4 columns for each bounding box edge.

    Parameters:
    -----------
    targets: list
     List of bounding boxes. Each box is represented as a list with the
     following format:

        Case 1 (confidence provided):
             ['image_name', 'x_min, 'y_min, x_max, y_max', 'confidence']
        Case 2 (confidence not provided):
             ['image_name', 'x_min, 'y_min, x_max, y_max']
        Case 3: (List with more than three elements)
            ['image_name', ... ]

    Returns:
    --------
    new_targets: list
        List following the following format:

         Case 1 (confidence provided):
             ['image_name', 'x_min', 'y_min', 'x_max', 'y_max', 'confidence']
         Case 2 (confidence not provided):
             ['image_name', 'x_min', 'y_min', 'x_max', 'y_max']
         Case 3: (List with more than three elements)
            ['image_name', ... ]
    """

    new_targets = []

    for target in targets:
        if len(target) == 2:
            new_targets.append([target[0]] + target[1].split(","))
        elif len(target) == 3:
            new_targets.append([target[0]] + target[1].split(",") + list(target[2:]))
        else:
            new_targets.append(target)

    return new_targets


def voc_ap(rec, prec, use_07_metric=False):
    """ ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    """
    if use_07_metric:
        # 11 point metric
        ap = 0.0
        for t in np.arange(0.0, 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.0
    else:
        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.concatenate(([0.0], rec, [1.0]))
        mpre = np.concatenate(([0.0], prec, [0.0]))

        # compute the precision envelope
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def objectDetectionAP(dets, gts, ovthresh=0.5, use_07_metric=False):
    """
    This function takes a list of ground truth boxes and a list of detected bounding boxes
    for a given class and computes the average precision of the detections with respect to
    the ground truth boxes.

    Parameters:
    -----------
    dets: list
     List of bounding box detections. Each box is represented as a list
     with format:
         Case 1 (confidence provided):
             ['image_name', 'x_min', 'y_min', 'x_max', 'y_max', 'confidence']
         Case 2 (confidence not provided):
             ['image_name', 'x_min', 'y_min', 'x_max', 'y_max']
         Case 3 (confidence provided, coordinates as string):
             ['image_name', 'x_min, 'y_min, x_max, y_max', 'confidence']
         Case 4 (confidence not provided, coordinates as string):
             ['image_name', 'x_min, 'y_min, x_max, y_max']

    gts: list
     List of ground truth boxes. Each box is represented as a list with the
     following format: [image_name, x_min, y_min, x_max, y_max].

    [ovthresh]: float
     Overlap threshold (default = 0.5)

    [use_07_metric]: boolean
     Whether to use VOC07's 11 point AP computation (default False)

    Returns:
    --------
    rec: 1d array-like
     Array where each element (rec[i]) is the recall when considering i+1 detections

    prec: 1d array-like
     Array where each element (rec[i]) is the precision when considering i+1 detections

    ap: float
     Average precision between detected boxes and the ground truth boxes.
     (it is also the area under the precision-recall curve).

    Example:

    With confidence scores:
    >> predictions_list = [['img_00285.png',330,463,387,505,0.0739],
                           ['img_00285.png',420,433,451,498,0.0910],
                           ['img_00285.png',328,465,403,540,0.1008],
                           ['img_00285.png',480,477,508,522,0.1012],
                           ['img_00285.png',357,460,417,537,0.1058],
                           ['img_00285.png',356,456,391,521,0.0843],
                           ['img_00225.png',345,460,415,547,0.0539],
                           ['img_00225.png',381,362,455,513,0.0542],
                           ['img_00225.png',382,366,416,422,0.0559],
                           ['img_00225.png',730,463,763,583,0.0588]]
    >> ground_truth_list = [['img_00285.png',480,457,515,529],
                            ['img_00285.png',480,457,515,529],
                            ['img_00225.png',522,540,576,660],
                            ['img_00225.png',739,460,768,545]]

    >> rec, prec, ap = objectDetectionAP(predictions_list, ground_truth_list)
    >> print(ap)
    0.125

    Without confidence scores:
    >> predictions_list = [['img_00285.png',330,463,387,505],
                           ['img_00285.png',420,433,451,498],
                           ['img_00285.png',328,465,403,540],
                           ['img_00285.png',480,477,508,522],
                           ['img_00285.png',357,460,417,537],
                           ['img_00285.png',356,456,391,521],
                           ['img_00225.png',345,460,415,547],
                           ['img_00225.png',381,362,455,513],
                           ['img_00225.png',382,366,416,422],
                           ['img_00225.png',730,463,763,583]]
    >> ground_truth_list = [['img_00285.png',480,457,515,529],
                            ['img_00285.png',480,457,515,529],
                            ['img_00225.png',522,540,576,660],
                            ['img_00225.png',739,460,768,545]]

    >> rec, prec, ap = objectDetectionAP(predictions_list, ground_truth_list)
    >> print(ap)
    0.0625

    """

    # Unvectorize the detected bounding boxes
    dets = unvectorize(dets)
    gts = unvectorize(gts)

    # Load ground truth
    gt_dict = group_gt_boxes_by_image_name(gts)

    # extract gt objects for this class
    recs = {}
    npos = 0

    imagenames = sorted(gt_dict.keys())
    for imagename in imagenames:
        R = [obj for obj in gt_dict[imagename]]
        bbox = np.array([x["bbox"] for x in R])
        det = [False] * len(R)
        npos = npos + len(R)
        recs[imagename] = {"bbox": bbox, "det": det}

    # Load detections
    det_length = len(dets[0])

    # Check that all boxes are the same size
    for det in dets:
        assert len(det) == det_length, "Not all boxes have the same dimensions."

    image_ids = [x[0] for x in dets]
    BB = np.array([[float(z) for z in x[1:5]] for x in dets])

    if det_length == 6:
        logging.info("confidence scores are present")
        confidence = np.array([float(x[-1]) for x in dets])
        # sort by confidence
        sorted_ind = np.argsort(-confidence)

    else:
        logging.info("confidence scores are not present")
        num_dets = len(dets)
        sorted_ind = np.arange(num_dets)

    BB = BB[sorted_ind, :]
    image_ids = [image_ids[x] for x in sorted_ind]

    # go down dets and mark TPs and FPs
    nd = len(image_ids)
    tp = np.zeros(nd)
    fp = np.zeros(nd)
    for d in range(nd):
        R = recs[image_ids[d]]
        bb = BB[d, :].astype(float)
        ovmax = -np.inf
        BBGT = R["bbox"].astype(float)

        if BBGT.size > 0:
            # compute overlaps
            # intersection
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            iw = np.maximum(ixmax - ixmin + 1.0, 0.0)
            ih = np.maximum(iymax - iymin + 1.0, 0.0)
            inters = iw * ih

            # union
            uni = (
                (bb[2] - bb[0] + 1.0) * (bb[3] - bb[1] + 1.0)
                + (BBGT[:, 2] - BBGT[:, 0] + 1.0) * (BBGT[:, 3] - BBGT[:, 1] + 1.0)
                - inters
            )

            overlaps = inters / uni
            ovmax = np.max(overlaps)
            jmax = np.argmax(overlaps)

        if ovmax > ovthresh:
            if not R["det"][jmax]:
                # print('Box matched!')
                tp[d] = 1.0
                R["det"][jmax] = 1
            else:
                # print('Box was already taken!')
                fp[d] = 1.0
        else:
            # print('No match with sufficient overlap!')
            fp[d] = 1.0

    # compute precision recall
    fp = np.cumsum(fp)
    tp = np.cumsum(tp)
    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = voc_ap(rec, prec, use_07_metric)

    return rec, prec, ap
