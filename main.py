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


def main(item, n=100, data_dir=DATA_DIR):
    wnid = get_wnid(item)
    if not os.path.exists(os.path.join(data_dir, item)):
        os.mkdir(os.path.join(data_dir, item))

    urls = get_image_urls(wnid)
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
            # print(e)
            continue

        headers = image.headers
        if image.status_code != 200:
            # print("\tCONNECTION ERROR {}: {}".format(image.status_code, url))
            continue
        elif headers['Content-Type'] != 'image/jpeg':
            # print("\tFILE TYPE ERROR {}: {}".format(headers['Content-Type'], url))
            continue
        elif int(headers['Content-Length']) < 50000:  # only files > 50kb
            # print("\tFILE SIZE ERROR {}: {}".format(headers['Content-Length'], url))
            continue
        else:
            write_to_file(file_path, image.content)
            pbar.update()
            images += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "item",
        help="What image do you want to search for?",
        type=str,
    )
    parser.add_argument(
        '-n',
        type=int,
        default=100,
    )
    parser.add_argument(
        '-dir',
        type=str,
        default=DATA_DIR,
    )
    args = parser.parse_args()
    item = args.item
    n = args.n
    dir = args.dir
    if not os.path.exists(dir):
        os.mkdir(dir)

    main(item, n, dir)
