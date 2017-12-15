#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Functions for generating PR-curve axis and calculating AP and mean AP
#

import math
from statistics import mean
import numpy as np
import scipy.interpolate

from .util import *

__all__ = ['pr', 'ap', 'mean_ap']


def pr(detections, ground_truth, overlap_threshold=0.5, class_label_map=None):
    """ Compute precision and recall values for multiple classes

        detections          -- dict of detections per image (eg. parse())
        ground_truth        -- dict of annotations per image (eg. parse())
        overlap_threshold   -- minimum iou value needed to count detection as true positive
        class_label_map     -- list of classes you want to compute PR (default: all classes)

        Returns dict of (p,r) tuples for every class, dict key is the class label
    """
    return graph(detections, ground_truth, overlap_threshold, class_label_map, pr_single)


def pr_single(detection_results, ground_truth, overlap_threshold):
    """ Compute a list of precision recall values that can be plotted into a graph

        detection_results   -- dict of detection objects per image
        ground_truth        -- dict of annotation objects per image
        overlap_threshold   -- minimum iou threshold for true positive

        Returns precision, recall
    """

    tps, fps, num_annotations, _ = match_for_graphs(detection_results, ground_truth, overlap_threshold)

    precision = []
    recall = []
    for tp, fp in zip(tps, fps):
        recall.append(tp / num_annotations)
        precision.append(tp / (fp + tp))

    return precision, recall


def ap(precision, recall, num_of_samples=100):
    """ Compute the average precision from a given pr-curve
        The average precision is defined as the area under the curve

        precision           -- list of precision values
        recall              -- list of recall values
        num_of_samples      -- number of samples to take from the curve to measure the average precision
    """
    samples = np.arange(0., 1., 1.0/num_of_samples)
    if len(p) > 1 and len(r) > 1:
        p = np.array(precision)
        r = np.array(recall)
        interpolated = scipy.interpolate.interp1d(r, p, fill_value=(1., 0.), bounds_error=False)(samples)
        avg = sum(interpolated) / len(interpolated)
    elif len(p) > 0 and len(r) > 0:
        # 1 point on PR: AP is box between (0,0) and (p,r)
        avg = precision[0] * recall[0]
    else:
        # Should never happen (graph filters out classes where no det/gt are found)
        avg = float('nan')
    return avg


def mean_ap(pr, num_of_samples=100):
    """ Compute mean average precision over the classes

        pr                  -- dict containing (p,r) tuples per class (eg. pr())
        num_of_samples      -- number of samples to take from the curve to measure the average precision
    """
    aps = [ap(p, r, num_of_samples) for _, (p, r) in pr.items()]
    aps = [ap for ap in aps if not math.isnan(ap)]
    return mean(aps)
