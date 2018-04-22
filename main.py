import os
import argparse

import requests
import numpy as np
from tqdm import tqdm

from imagenet.utils import downloader


DATA_DIR = 'images/'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'item',
        help='image to download images of',
        type=str,
    )
    parser.add_argument(
        '-n',
        help='number of images to download',
        type=int,
        default=100,
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
    item = args.item
    n = args.n
    dir = args.dir
    size = args.size
    shuffle = args.shuffle * 1000  # to convert to kb

    if not os.path.exists(dir):
        os.mkdir(dir)

    downloader(item, n, data_dir=dir, file_size=size, shuffle=shuffle)
