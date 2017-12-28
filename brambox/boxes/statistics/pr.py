#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#   Author: Tanguy Ophoff
#
#   Functions for generating PR-curve values and calculating average precision
#

import math
from statistics import mean
import numpy as np
import scipy.interpolate

from .util import *

__all__ = ['pr', 'ap']


def pr(detections, ground_truth, overlap_threshold=0.5):
    """ Compute a list of precision recall values that can be plotted into a graph

        detections   -- dict of detection objects per image
        ground_truth        -- dict of annotation objects per image
        overlap_threshold   -- minimum iou threshold for true positive

        Returns precision, recall
    """
    tps, fps, num_annotations = match_detections(detections, ground_truth, overlap_threshold)

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
    if len(precision) > 1 and len(recall) > 1:
        p = np.array(precision)
        r = np.array(recall)
        samples = np.arange(0., 1., 1.0/num_of_samples)
        interpolated = scipy.interpolate.interp1d(r, p, fill_value=(1., 0.), bounds_error=False)(samples)
        avg = sum(interpolated) / len(interpolated)
    elif len(precision) > 0 and len(recall) > 0:
        # 1 point on PR: AP is box between (0,0) and (p,r)
        avg = precision[0] * recall[0]
    else:
        avg = float('nan')

    return avg
