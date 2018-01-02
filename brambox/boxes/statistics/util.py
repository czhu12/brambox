#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Common functions for this package
#

__all__ = ['iou', 'ioa', 'match_detections']


def iou(a, b):
    """Calculate the intersection over union between two boxes
    The function returns the IUO value which is defined as:
    IOU = intersection(a, b) / (area(a) + area(b) - intersection(a, b))

    a   -- first box
    b   -- second box
    """
    intersection_area = intersection(a, b)
    union_area = a.width * a.height + b.width * b.height - intersection_area

    return intersection_area / union_area


def ioa(a, b, denominator='b'):
    """ Calculate the intersection over area between two boxes a and b.
    The function returns the value which is defined as:
    IOB = intersection(a, b) / (area(selected_box))
    """
    if denominator == 'min':
        div = min(a.width * a.height, b.width * b.height)
    elif denominator == 'max':
        div = max(a.width * a.height, b.width * b.height)
    elif denominator == 'a':
        div = a.width * a.height
    else:
        div = b.width * b.height

    return intersection(a, b) / div


def match_detections(detection_results, ground_truth, overlap_threshold, overlap_fn=iou):
    """ Match detection results with gound truth and return true and false positive rates

        detection_results   -- dict of detection objects per image
        ground_truth        -- dict of annotation objects per image
        overlap_threshold   -- minimum iou threshold for true positive
        overlap_fn          -- overlap area calculation function

        Returns the following stats:

        tps                 -- a list of true positive values
        fps                 -- a list of false positive values
        num_annotations     -- integer with the number of included annotations
    """
    all_matches = []
    num_annotations = 0

    # Make copy to not alter the reference
    detection_results = detection_results.copy()

    # make sure len(detection_results) == len(ground_truth) by inserting empty detections lists
    for image_id, annotations in ground_truth.items():
        if image_id not in detection_results:
            detection_results[image_id] = []

    for image_id, detections in detection_results.items():
        # Split ignored annotations
        annotations = []
        ignored_annotations = []
        for annotation in ground_truth[image_id][:]:
            if annotation.ignore:
                ignored_annotations.append(annotation)
            else:
                annotations.append(annotation)
        num_annotations += len(annotations)

        # Match detections
        detections = sorted(detections, key=lambda d: d.confidence, reverse=True)
        for detection in detections:
            matched_annotation = match_detection_to_annotations(detection, annotations, overlap_threshold, overlap_fn)
            if matched_annotation is not None:
                del annotations[matched_annotation]
                all_matches.append((detection.confidence, True))
            elif match_detection_to_annotations(detection, ignored_annotations, overlap_threshold, ioa) is None:
                all_matches.append((detection.confidence, False))

    # sort matches by confidence from high to low
    all_matches = sorted(all_matches, key=lambda d: d[0], reverse=True)

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

    return tps, fps, num_annotations


def intersection(a, b):
    """ Calculate the intersection area between two boxes """
    intersection_top_left_x = max(a.x_top_left, b.x_top_left)
    intersection_top_left_y = max(a.y_top_left, b.y_top_left)
    intersection_bottom_right_x = min(a.x_top_left + a.width,  b.x_top_left + b.width)
    intersection_bottom_right_y = min(a.y_top_left + a.height, b.y_top_left + b.height)

    intersection_width = intersection_bottom_right_x - intersection_top_left_x
    intersection_height = intersection_bottom_right_y - intersection_top_left_y

    if intersection_width <= 0 or intersection_height <= 0:
        return 0.0

    return intersection_width * intersection_height


def match_detection_to_annotations(detection, annotations, overlap_threshold, overlap_fn):
    """ Compute the best match (largest overlap area) between a given detection and
    a list of annotations.
    detection           -- detection to match
    annotations         -- annotations to search for the best match
    overlap_threshold   -- minimum overlap area to consider a match
    overlap_fn          -- overlap area calculation function
    """
    best_overlap = overlap_threshold
    best_annotation = None
    for i, annotation in enumerate(annotations):
        if annotation.class_label != detection.class_label:
            continue

        overlap = overlap_fn(annotation, detection)
        if overlap < best_overlap:
            continue
        best_overlap = overlap
        best_annotation = i

    return best_annotation
