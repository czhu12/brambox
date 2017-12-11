#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
#   Common functions for this package
#

__all__ = ['iou', 'iob', 'graph', 'match_for_graphs']


def intersection(a, b):
    """Calculate the intersection area between two boxes
    """
    intersection_top_left_x = max(a.x_top_left, b.x_top_left)
    intersection_top_left_y = max(a.y_top_left, b.y_top_left)
    intersection_bottom_right_x = min(a.x_top_left + a.width,  b.x_top_left + b.width)
    intersection_bottom_right_y = min(a.y_top_left + a.height, b.y_top_left + b.height)

    intersection_width = intersection_bottom_right_x - intersection_top_left_x
    intersection_height = intersection_bottom_right_y - intersection_top_left_y

    if intersection_width <= 0 or intersection_height <= 0:
        return 0.0

    return intersection_width * intersection_height


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


def iob(a, b):
    """Calculate the intersection over b between two boxes
    The function returns the value which is defined as:
    IOB = intersection(a, b) / (area(b))
    """
    return intersection(a, b) / (b.width * b.height)


def graph(detections, ground_truth, overlap_threshold, class_label_map, graph_fun):
    """ Compute graph axis values for multiple classes

        detections          -- dict of detections per image (eg. parse())
        ground_truth        -- dict of annotations per image (eg. parse())
        overlap_threshold   -- minimum iou value needed to count detection as true positive
        class_label_map     -- list of classes you want to compute PR (default: all classes)
        graph_fun           -- function to calculate the graph axis values

        Returns dict of (p,r) tuples for every class, dict key is the class label
    """
    # Get unique class_label_map
    if class_label_map is not None:
        classes = set(class_label_map)
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
        result[label] = graph_fun(det_filtered, gt_filtered, overlap_threshold)

    return result


def match_detection_to_annotations(detection, annotations, overlap_threshold, oa=iou):
    """calculate the best match (largest overlap area) between a given detection and
    a list of annotations.
    detection           -- detection to match
    annotations         -- annotations to search for the best match
    overlap_threshold   -- minimum overlap area to consider a match
    oa                  -- overlap area calculation function
    """
    best_overlap = overlap_threshold
    best_annotation = None
    for annotation in annotations:
        overlap = oa(annotation, detection)
        if overlap < best_overlap:
            continue
        best_overlap = overlap
        best_annotation = annotation

    return best_annotation


def match_for_graphs(detection_results, ground_truth, overlap_threshold):
    """ Match detection results with gound truth for calculating PR and MR_FPPI curves

        detection_results   -- dict of detection objects per image
        ground_truth        -- dict of annotation objects per image
        overlap_threshold   -- minimum iou threshold for true positive

        Returns the following stats:

        tps                 -- a list of true positive values
        fps                 -- a list of false positive values
        num_annotations     -- integer with the number of included annotations
        num_images          -- integer with the number of processed images
    """
    all_matches = []
    num_annotations = 0

    # Make copy to not alter the reference
    detection_results = detection_results.copy()

    # make sure len(detection_results) == len(ground_truth) by inserting empty detections lists
    for image_id, annotations in ground_truth.items():
        if image_id not in detection_results:
            detection_results[image_id] = []

    # run over every image
    for image_id, detections in detection_results.items():

        annotations = []
        ignored_annotations = []
        # [:] is to copy the annotations instead of returning a reference
        for annotation in ground_truth[image_id][:]:
            if annotation.ignore:
                ignored_annotations += [annotation]
            else:
                annotations += [annotation]

        num_annotations += len(annotations)
        # sort detections by confidence, highest confidence first
        detections = sorted(detections, key=lambda d: d.confidence, reverse=True)

        for detection in detections:
            matched_annotation = match_detection_to_annotations(detection, annotations, overlap_threshold, iou)
            if matched_annotation is not None:
                annotations.remove(matched_annotation)
                all_matches.append((detection.confidence, True))
            elif match_detection_to_annotations(detection, ignored_annotations, overlap_threshold, iob) is None:
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

    return tps, fps, num_annotations, len(ground_truth)
