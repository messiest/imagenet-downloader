import os
import requests
import argparse

from tqdm import tqdm
import numpy as np

from nltk.corpus import wordnet as wn


DATA_DIR = 'images/'


def get_wnid(term, user=False):
    assert isinstance(term, str), "Must pass string"
    syns = wn.synsets(term.lower())
    if user:
        print(term.capitalize(), ":")
        d = {str(i+1): j for i, j in enumerate(syns)}
        for k in d:
            print('\t{}) {}'.format(k, d[k].definition()))
        choice = input("Choose word to search for: ")
        assert choice in d.keys(), "You must choose from the definitions above."
        syn = d[choice]
    else:
        syn = syns.pop(0)
    wnid = syn.offset()

    return wnid


def get_image_urls(wnid, shuffle=False):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """
    print("Fetching image urls...")
    image_urls = []

    # image net search id
    api_url = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n0{}"
    url = api_url.format(wnid)
    html = requests.get(url)  # html for search
    urls = (image_url for image_url in html.text.split('\r\n') if image_url)
    image_urls = [url.split()[1] for url in urls if url != '\n']

    if shuffle:
        np.random.shuffle(image_urls)  # randomize order

    return image_urls


def write_to_file(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)


def downloader(item, n=100, data_dir=DATA_DIR, file_size=50000, timeout=2, shuffle=False, user_input=False):
    wnid = get_wnid(item, user_input)
    if not os.path.exists(os.path.join(data_dir, item)):
        os.mkdir(os.path.join(data_dir, item))

    urls = get_image_urls(wnid, shuffle=shuffle)
    pbar = tqdm(total=n, desc="Downloading {} Images".format(item.capitalize()), leave=True, unit='image')
    images = 0
    n = np.min((n, len(urls)))  # ensure number of images is attainable
    while images <= n and urls:
        url = urls.pop(0)
        file_name = url.split('/')[-1]
        file_path = os.path.join(data_dir, item, file_name)
        try:
            image = requests.get(url, allow_redirects=False, timeout=timeout)
        except Exception as e:
            tqdm.write("{} | {}".format(str(e.__doc__), url))
            continue

        # error handling
        headers = image.headers
        try:
            if image.status_code != 200:
                tqdm.write("connection error {} | {}".format(image.status_code, url))
                continue
            elif headers['Content-Type'] != 'image/jpeg':
                tqdm.write("file type error {} | {}".format(headers['Content-Type'], url))
                continue
            elif int(headers['Content-Length']) < file_size:  # min file size
                tqdm.write("file size error {} | {}".format(headers['Content-Length'], url))
                continue
            else:
                write_to_file(file_path, image.content)
                pbar.update()
                images += 1
        except:
            continue
    pbar.close()


if __name__ == "__main__":
    wnid = get_wnid('dog')
    print("WNID:", wnid)
    urls = get_image_urls(wnid)
    print("Total URLs", len(urls))
