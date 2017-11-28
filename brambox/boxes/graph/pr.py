#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

import numpy as np
import scipy.interpolate

__all__ = ['get_pr', 'get_average_precision']


def get_pr(detection_results, ground_truth, overlap_threshold=0.5):
    """Calculate a list of precision recall values that can be plotted into a graph
    detection_results   -- dict of detection objects per image
    ground_truth        -- dicht of annotation objects per image
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
                overlap = get_iou(annotation, detection)
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


def get_average_precision(precision, recall, num_of_samples=100):
    """Calculate the average precision from a given pr-curve
    The average precision is defined as the area under the curve
    precision   -- list of precision values
    recall      -- list of recall values
    samples     -- number of samples to take from the curve to measure the average precision
    """
    samples = np.arange(0., 1., 1.0/num_of_samples)
    p = np.array(precision)
    r = np.array(recall)
    interpolated = scipy.interpolate.interp1d(r, p, fill_value=(1., 0.), bounds_error=False)(samples)
    avg = sum(interpolated) / len(interpolated)
    return avg


def get_iou(a, b):
    """Calculate the intersection over union between two boxes
    a -- first box
    b -- second box
    The function returns the IUO value which is defined as:
    IOU = intersection(a, b) / (area(a) + area(b) - intersection(a, b))
    """

    intersection_top_left_x = max(a.x_top_left, b.x_top_left)
    intersection_top_left_y = max(a.y_top_left, b.y_top_left)
    intersection_bottom_right_x = min(a.x_top_left + a.width,  b.x_top_left + b.width)
    intersection_bottom_right_y = min(a.y_top_left + a.height, b.y_top_left + b.height)

    intersection_width = intersection_bottom_right_x - intersection_top_left_x
    intersection_height = intersection_bottom_right_y - intersection_top_left_y

    if intersection_width <= 0 or intersection_height <= 0:
        return 0.0

    intersection_area = intersection_width * intersection_height
    union_area = a.width * a.height + b.width * b.height - intersection_area

    return intersection_area / union_area
