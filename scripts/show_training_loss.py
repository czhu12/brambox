#!python
import re
import argparse
import matplotlib.pyplot as plt


class Batch:
    def __init__(self, iteration, total_loss, avg_loss):
        self.iteration = iteration
        self.total_loss = total_loss
        self.avg_loss = avg_loss

    def __str__(self):
        text = "iteration = {}, ".format(self.iteration)
        text += "total loss = {}, ".format(self.total_loss)
        text += "avg_loss = {}".format(self.avg_loss)
        return text


def main():

    parser = argparse.ArgumentParser(description='Parse darknet stdout, plot the loss and indicate weigts file with lowest avg precision and total precision')
    parser.add_argument('input', help='Input text file containing darknet stdout')
    parser.add_argument('--weights-step', default=100, help=('Multiple of iterations a new weigts file is saved. This is used to point to the most interesting weights file'))
    args = parser.parse_args()

    with open(args.input) as f:
        text = f.read()

    # clean up output by removing 'Saving weights to .*\.weights'
    text = re.sub(r'Saving weights to .*\.weights\n', '', text)

    # parse text file
    values = []
    lines = text.split('\n')
    for line in lines:
        if line.endswith('images'):
            elements = line.split()
            iteration = int(elements[0].strip(':'))
            total_loss = float(elements[1].strip(','))
            avg_loss = float(elements[2])
            values.append(Batch(iteration, total_loss, avg_loss))

    # find optimal weight file candidates
    subsampled_values = [v for v in values if v.iteration % args.weights_step == 0]
    sorted_subsampled_values = sorted(subsampled_values, key=lambda v: v.avg_loss)
    for i in range(10):
        print("Candidate", i+1, "=", sorted_subsampled_values[i])

    # plot loss
    total_losses = [v.total_loss for v in values]
    avg_losses = [v.avg_loss for v in values]
    iterations = [v.iteration for v in values]

    plt.figure(figsize=(10, 8))
    plt.plot(iterations, total_losses, label="total loss", linewidth=1)
    plt.plot(iterations, avg_losses, label="avg loss", linewidth=1)

    plt.gcf().suptitle('Training loss', weight='bold')
    plt.gca().set_ylabel('Loss')
    plt.gca().set_xlabel('Iteration')
    plt.gca().set_ylim([0, 10])
    plt.gca().set_xlim(left=0)
    plt.show()


if __name__ == '__main__':
    main()
