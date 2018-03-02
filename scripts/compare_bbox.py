#!python
import time
import argparse
from pathlib import Path
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
    colors = [
        (255, 0, 0),
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 0),
        (255, 255, 255),
        (0, 0, 0)
    ]

    def __init__(self, args):
        self.annoname, fmt = self._split_format_path(args.anno)
        self.annos = bbb.parse(fmt, self.annoname, **args.kwargs)
        self.ids = sorted(list(self.annos.keys()))

        self.dets = []
        self.detnames = []
        if args.det is not None:
            for det in args.det:
                name, fmt = self._split_format_path(det)
                self.detnames.append(name)
                self.dets.append(bbb.parse(fmt, name, **args.kwargs))

        self.folder = args.imagefolder
        self.ext = args.extension
        if args.extension != "" and args.extension[0] != '.':
            self.ext = '.' + args.extension

        self.anno_labels = args.show_anno_labels
        self.det_labels = args.show_det_labels

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, idx):
        """ Returns (id, img) tuple """
        img_idx = self.ids[idx]
        img_path = Path(self.folder) / (img_idx + self.ext)
        anno = self.annos[img_idx]

        img = bbb.draw_boxes(img_path, anno, show_labels=self.anno_labels, color=self.colors[0])
        for i, det in enumerate(self.dets):
            color_idx = (i % (len(self.colors)-1)) + 1
            if img_idx in det:
                ok, nok = bbb.filter_split(det[img_idx], bbb.MatchFilter(anno))
                bbb.draw_boxes(img, ok, show_labels=self.det_labels, color=self.colors[color_idx])
                bbb.draw_boxes(img, nok, show_labels=self.det_labels, color=self.colors[color_idx], faded=lambda b: True)

        return img_idx, img

    def _split_format_path(self, s):
        if ':' in s:
            return s.split(':', maxsplit=1)
        else:
            raise ValueError('No format specified [{s}]')


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
        boxes = imgs.annos[imgs.ids[number]]
        name = False
        for box in boxes:
            if not name:
                print(f'{imgs.annoname}')
                name = True
            if detailed:
                print(f'\t {repr(box)}')
            else:
                print(f'\t {box}')
        for i, det in enumerate(imgs.dets):
            if imgs.ids[number] in det:
                name = False
                for box in det[imgs.ids[number]]:
                    if not name:
                        print(f'{imgs.detnames[i]}')
                        name = True
                    if detailed:
                        print(f'\t {repr(box)}')
                    else:
                        print(f'\t {box}')
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
        description='This script can be used to compare multiple bounding box files, like annotations and detections',
        usage='%(prog)s imagesfolder annofile:format [detfile:format detfile:format ...] [optional arguments]',
        epilog='Press \'?\' in the GUI for more information about the different keybindings'
    )

    parser.add_argument('imagefolder', help='Image folder')
    parser.add_argument('anno', metavar='annofile:format', help='Annotation format and file, folder or file sequence')
    parser.add_argument('det', metavar='detfile:format', help='Detection format and file, folder or file sequence', nargs='*')
    parser.add_argument('--extension', '-x', metavar='.ext', help='Image extension (default .png)', default='.png')
    parser.add_argument('--show-anno-labels', '-a', help='Show labels of annotations', action='store_true')
    parser.add_argument('--show-det-labels', '-d', help='Show labels of detections', action='store_true')
    parser.add_argument('--kwargs', metavar='KW=V', help='Keyword arguments for the parsers', nargs='*', action=StoreKwargs, default={})
    args = parser.parse_args()

    print('Parsing bounding boxes...')

    # Setup variables
    imgs = BoxImages(args)
    number = 0
    stride = 10

    print(f'Parsed {len(imgs.annos)} images')

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
