import os
import argparse

from imagenet.utils import downloader


DATA_DIR = 'images/cifar10'

CIFAR10 = [
    'airplane',
    'automobile',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck',
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        help='number of images to download',
        type=int,
        default=250,
    )
    parser.add_argument(
        '-dir',
        help='directory to save images',
        type=str,
        default=DATA_DIR,
    )
    parser.add_argument(
        '-size',
        help='minimum size of files in kb',
        type=int,
        default=50,
    )
    parser.add_argument(
        '-shuffle',
        help='randomize image urls for download',
        type=bool,
        default=False,
    )

    args = parser.parse_args()
    n = args.n
    dir = args.dir
    size = args.size
    shuffle = args.shuffle * 1000  # to convert to kb

    if not os.path.exists(dir):
        os.mkdir(dir)

    for item in CIFAR10:
        downloader(item, n, data_dir=dir, user_input=False)
