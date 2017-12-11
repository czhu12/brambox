#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Functions for generating miss-rate vs FPPI curves (False Positives Per Image) axis
#   and calculating log average miss-rate
#
import numpy as np
import scipy.interpolate

from .util import *

__all__ = ['mr_fppi', 'lamr', 'mean_lamr']


def mr_fppi(detections, ground_truth, overlap_threshold=0.5, class_label_map=None):
    """ Compute miss-rate vs FPPI values for multiple classes

        detections          -- dict of detections per image (eg. parse())
        ground_truth        -- dict of annotations per image (eg. parse())
        overlap_threshold   -- minimum iou value needed to count detection as true positive
        class_label_map     -- list of classes you want to compute PR (default: all classes)

        Returns dict of (mr,fppi) tuples for every class, dict key is the class label
    """
    return graph(detections, ground_truth, overlap_threshold, class_label_map, mr_fppi_single)


def mr_fppi_single(detection_results, ground_truth, overlap_threshold):
    """ Compute a list of miss-rate FPPI values that can be plotted into a graph

        detection_results   -- dict of detection objects per image
        ground_truth        -- dict of annotation objects per image
        overlap_threshold   -- minimum iou threshold for true positive

        Returns precision, recall
    """

    tps, fps, num_annotations, num_images = match_for_graphs(detection_results, ground_truth, overlap_threshold)

    miss_rate = []
    fppi = []
    for tp, fp in zip(tps, fps):
        miss_rate.append(1 - (tp / num_annotations))
        fppi.append(fp / num_images)

    return miss_rate, fppi


def lamr(miss_rate, fppi, num_of_samples=9):
    """ Compute the log average miss-rate from a given MR-FPPI curve
        The log average miss-rate is defined as the average of a number of evenly spaced log miss-rate
        samples on the log FPPI axis within the range [10^-2, 10^0]

        miss_rate           -- list of miss-rate values
        fppi                -- list of FPPI values
        num_of_samples      -- number of samples to take from the curve to measure the average precision
    """
    samples = np.logspace(-2., 0., num_of_samples)
    m = np.array(miss_rate)
    f = np.array(fppi)
    interpolated = scipy.interpolate.interp1d(f, m, fill_value=(1., 0.), bounds_error=False)(samples)
    log_interpolated = np.log(interpolated)
    avg = sum(log_interpolated) / len(log_interpolated)
    return np.exp(avg)


def mean_lamr():
    """TODO
    """
    raise NotImplementedError
