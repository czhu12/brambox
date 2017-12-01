#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

from statistics import mean
import numpy as np
import scipy.interpolate

from .util import *

__all__ = ['pr', 'ap', 'mean_ap']


def pr(detections, ground_truth, overlap_threshold=0.5, class_labels=None):
    """ Compute precision and recall values for all the classes

        detections          -- dict of detections per image (eg. parse())
        ground_truth        -- dict of annotations per image (eg. parse())
        overlap_threshold   -- minimum iou value needed to count detection as true positive
        class_labels        -- list of classes you want to compute PR (default: all classes)

        Returns dict of (p,r) tuples for every class
    """
    # Get unique class_labels
    if class_labels is not None:
        classes = set(class_labels)
    else:
        classes = set()
        for key, val in ground_truth.items():
            for box in val:
                classes.add(box.class_label)
        for key, val in detections.items():
            for box in val:
                classes.add(box.class_label)

    # Compute PR for every class
    result = {}
    for label in classes:
        det_filtered = {key: list(filter(lambda box: box.class_label == label, val)) for key, val in detections.items()}
        gt_filtered = {key: list(filter(lambda box: box.class_label == label, val)) for key, val in ground_truth.items()}
        result[label] = pr_single(det_filtered, gt_filtered, overlap_threshold)

    return result


def pr_single(detection_results, ground_truth, overlap_threshold):
    """ Compute a list of precision recall values that can be plotted into a graph

        detection_results   -- dict of detection objects per image
        ground_truth        -- dict of annotation objects per image
        overlap_threshold   -- minimum iou threshold for true positive

        Returns precision, recall
    """
    found = 0

    all_matches = []
    num_detections = 0
    num_annotations = 0

    # make sure len(detection_results) == len(ground_truth) by inserting empty detections lists
    for image_id, annotations in ground_truth.items():
        if image_id not in detection_results:
            detection_results[image_id] = []
        num_annotations += len(annotations)

    # run over every image
    for image_id, detections in detection_results.items():

        # [:] is to copy the annotations instead of returning a reference
        annotations = ground_truth[image_id][:]

        # sort detections by confidence, highest confidence first
        detections = sorted(detections, key=lambda d: d.confidence, reverse=True)

        num_detections += len(detections)
        for detection in detections:
            best_overlap = overlap_threshold
            best_annotation = None
            for annotation in annotations:
                overlap = iou(annotation, detection)
                if overlap < best_overlap:
                    continue
                best_overlap = overlap
                best_annotation = annotation

            if best_annotation is not None:
                annotations.remove(best_annotation)
                all_matches.append((detection.confidence, True))
            else:
                all_matches.append((detection.confidence, False))

    # sort matches by confidence from high to low
    all_matches = sorted(all_matches, key=lambda d: d[0], reverse=True)

    recall = []
    precision = []
    tps = []
    fps = []
    tp_counter = 0
    fp_counter = 0

    # all matches in dataset
    for det in all_matches:
        if det[1]:
            tp_counter += 1
        else:
            fp_counter += 1
        tps.append(tp_counter)
        fps.append(fp_counter)

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
    p = np.array(precision)
    r = np.array(recall)
    interpolated = scipy.interpolate.interp1d(r, p, fill_value=(1., 0.), bounds_error=False)(samples)
    avg = sum(interpolated) / len(interpolated)
    return avg


def mean_ap(pr, num_of_samples=100):
    """ Compute mean average precision over the classes

        pr                  -- dict containing (p,r) tuples per class (eg. pr())
        num_of_samples      -- number of samples to take from the curve to measure the average precision
    """
    return mean([ap(p, r, num_of_samples) for _, (p, r) in pr.items()])
