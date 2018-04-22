import requests
import argparse

from nltk.corpus import wordnet as wn


def get_wnid(term):
    assert isinstance(term, str), "Must pass string"
    syns = wn.synsets(term.lower())

    d = {str(i+1): j for i, j in enumerate(syns)}
    for k in d:
        print('{} - {}: {}'.format(k, term.capitalize(), d[k].definition()))
    choice = input("Choose word to search for: ")

    # syn = syns.pop(0)
    syn = d[choice]
    print("{}: {}".format(term.capitalize(), d[k].definition()))
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


if __name__ == "__main__":
    wnid = get_wnid('dog')
    print("WNID:", wnid)
    urls = get_image_urls(wnid)
    print("Total URLs", len(urls))
