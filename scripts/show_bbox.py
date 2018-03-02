#!python
import os
import time
import argparse
import brambox.boxes as bbb
import matplotlib.pyplot as plt

keys = {
    'next': ['right', 'd', 'l', ' '],
    'prev': ['left', 'a', 'h'],
    'next-stride': ['ctrl+right', 'ctrl+d', 'ctrl+l', 'cmd+right', 'cmd+d', 'cmd+l'],
    'prev-stride': ['ctrl+left', 'ctrl+a', 'ctrl+h', 'cmd+left', 'cmd+a', 'cmd+h'],
    'increment-stride': ['up', 'w', 'k'],
    'decrement-stride': ['down', 's', 'j'],
    'start': ['home', 'g'],
    'end': ['end', 'G'],
    'info': ['i'],
    'detailed-info': ['I'],
    'help': ['?'],
}


class StoreKwargs(argparse.Action):
    """ Store keyword arguments in a dict.
        This action must be used with multiple arguments.
        It will parse ints and floats and leave the rest as strings.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        d = {}
        for items in values:
            n, v = items.split('=')

            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass

            d[n] = v

        setattr(namespace, self.dest, d)


class BoxImages:
    def __init__(self, args):
        self.boxes = bbb.parse(args.format, args.file, **args.kwargs)
        self.ids = sorted(list(self.boxes.keys()))
        self.faded = eval(args.faded) if args.faded is not None else None

        self.folder = args.imagefolder
        self.ext = args.extension
        if args.extension != "" and args.extension[0] != '.':
            self.ext = '.' + args.extension
        self.labels = args.show_labels

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx):
        """ Returns (id, img) tuple """
        img_idx = self.ids[idx]
        img_path = os.path.join(self.folder, img_idx + self.ext)
        img = bbb.draw_boxes(img_path, self.boxes[img_idx], show_labels=self.labels, faded=self.faded)
        return img_idx, img


def on_key_press(event):
    global number
    global stride
    ignored_keys = ['alt', 'shift', 'None']

    if event.key in ignored_keys:
        return

    change = False
    if event.key in keys['prev']:
        change = True
        number -= 1
    elif event.key in keys['next']:
        change = True
        number += 1
    elif event.key in keys['prev-stride']:
        change = True
        number -= stride
    elif event.key in keys['next-stride']:
        change = True
        number += stride
    elif event.key in keys['decrement-stride']:
        if stride > 10:
            stride //= 10
        print(f'Stride: {stride}')
    elif event.key in keys['increment-stride']:
        if stride < 10000:
            stride *= 10
        print(f'Stride: {stride}')
    elif event.key in keys['start']:
        change = True
        number = 0
    elif event.key in keys['end']:
        change = True
        number = len(imgs)-1
    elif event.key in keys['info'] or event.key in keys['detailed-info']:
        detailed = True if event.key in keys['detailed-info'] else False
        boxes = imgs.boxes[imgs.ids[number]]
        for box in boxes:
            if detailed:
                print(repr(box))
            else:
                print(box)
        print()

    elif event.key in keys['help']:
        print(help())

    if change:
        while number < 0:
            number += len(imgs)
        while number >= len(imgs):
            number -= len(imgs)

        img_id, img = imgs[number]
        ax.clear()
        ax.set_title(img_id)
        ax.imshow(img)
        fig.canvas.draw()


def help():
    string = 'Key mapping:\n'
    for k, v in keys.items():
        string += f'  {k}: {v}\n'
    return string


def main():
    global number
    global stride
    global imgs
    global fig
    global ax

    parser = argparse.ArgumentParser(
        description='This script will display the provided bounding boxes on the images',
        usage='%(prog)s format file imagefolder [optional arguments]',
        epilog='Press \'?\' in the GUI for more information about the different keybindings'
    )

    parser.add_argument('format', metavar='format', help='format key form brambox.boxes.formats', choices=bbb.formats.keys())
    parser.add_argument('file', help='Bounding box file, folder or file sequence')
    parser.add_argument('imagefolder', help='Image folder')
    parser.add_argument('--extension', '-x', metavar='.ext', help='Image extension (default .png)', default='.png')
    parser.add_argument('--show-labels', '-l', help='Show labels above bounding boxes', action='store_true')
    parser.add_argument('--faded', '-f', metavar='lambda', help='Lambda function to pass as faded parameter', default=None)
    parser.add_argument('--kwargs', metavar='KW=V', help='Keyword arguments for the parser', nargs='*', action=StoreKwargs, default={})
    args = parser.parse_args()

    print('Parsing bounding boxes...')

    # Setup variables
    imgs = BoxImages(args)
    number = 0
    stride = 10

    print(f'Parsed {len(imgs.boxes)} images')

    # Setup pyplot
    plt.rcParams['keymap.all_axes'].remove('a')
    plt.rcParams['keymap.back'].remove('left')
    plt.rcParams['keymap.forward'].remove('right')
    plt.rcParams['keymap.home'].remove('h')
    plt.rcParams['keymap.save'].remove('s')
    plt.rcParams['keymap.xscale'] = []
    plt.rcParams['keymap.yscale'] = []
    fig = plt.figure('Brambox Bounding Boxes')
    ax = fig.gca()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    # Show first img
    print('\nVisualisation...')
    img_id, img = imgs[0]
    ax.set_title(img_id)
    ax.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
