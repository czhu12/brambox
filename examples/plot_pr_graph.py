#!python
import os
import brambox.boxes as bbb
import matplotlib.pyplot as plt

identify = lambda f: os.path.splitext("/".join(f.rsplit('/')[-3:]))[0]

def main():
    ground_truth = bbb.parse('anno_dollar', 'data/annotations/*/*/*.txt', identify)
    detection_results = bbb.parse('det_coco', 'data/coco_results.json')

    precision, recall = bbb.get_pr(detection_results, ground_truth, 0.4)
    ap = bbb.get_average_precision(precision, recall)

    plt.figure(figsize=(12, 10))
    plt.plot(recall, precision, label=f"Det (ap = {round(ap, 3)})", linewidth=2)
    plt.legend(loc=3)
    plt.gcf().suptitle('PR-curve plot example', weight='bold')
    plt.gca().set_ylabel('Precision')
    plt.gca().set_xlabel('Recall')
    plt.gca().set_xlim([0, 1])
    plt.gca().set_ylim([0, 1])
    plt.show()


if __name__ == '__main__':
    main()
