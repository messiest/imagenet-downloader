import os
import argparse

import requests
import numpy as np
from tqdm import tqdm

from imagenet.utils import get_wnid, get_image_urls, write_to_file


DATA_DIR = 'images/'


def write_to_file(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)


def main(item, n=100, data_dir=DATA_DIR, file_size=50000, shuffle=False):
    wnid = get_wnid(item)
    if not os.path.exists(os.path.join(data_dir, item)):
        os.mkdir(os.path.join(data_dir, item))

    urls = get_image_urls(wnid, shuffle=shuffle)
    pbar = tqdm(total=n, desc=item.capitalize(), unit='image')
    images = 0
    n = np.min((n, len(urls)))  # ensure number of images is attainable
    while images <= n and urls:
        url = urls.pop(0)
        file_name = url.split('/')[-1]
        file_path = os.path.join(data_dir, item, file_name)
        try:
            image = requests.get(url, allow_redirects=False, timeout=2)
        except Exception as e:
            continue

        # error handling
        headers = image.headers
        if image.status_code != 200:
            continue
        elif headers['Content-Type'] != 'image/jpeg':
            continue
        elif int(headers['Content-Length']) < file_size:  # only files > 50kb
            continue
        else:
            write_to_file(file_path, image.content)
            pbar.update()
            images += 1
    pbar.close()


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

    main(item, n, data_dir=dir, file_size=size, shuffle=shuffle)
