#!/usr/bin/env python3.6
import os
import csv
import asyncio

import numpy as np
import requests
from bs4 import BeautifulSoup
import nltk


DATA_DIR = './data/'  # where the data csv is stored
CIFAR10 = ['airplane', 'car', 'bird', 'cat', 'deer',  # automobile to car
           'dog', 'frog', 'horse', 'boat', 'truck']  # ship to boat


def get_image_urls(wnid):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """
    # print("Getting {} image urls...".format())

    image_urls = []
    print("TAGS: ", tags)
    for tag in tags:
        # image net search id
        api_url = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n0{}"
        url = api_url.format(tag)
        try:
            print("URL:", url)
            html = requests.get(url)  # html for search
            urls = (image_url for image_url in html.text.split('\r\n'))
            image_urls = [url for url in urls if url != '\n']
        except:
            pass

    # np.random.shuffle(image_urls)  # randomize order

    return image_urls


def build_collection(loop, data_dir, url, category):
    """
    build a csv of image urls

    :param loop: async event loop for the downloader
    :type loop: asyncio.AbstractEventLoop()
    :param data_dir: key for the image file, used as the file name
    :type data_dir: str
    :param url: url to the image file
    :type url: str
    :param category: category for the image, used to save to a class directory
    :type category: str
    :return: None
    :rtype: None
    """
    with open(os.path.join(data_dir, 'images.csv'), 'a') as file:
        writer = csv.writer(file)
        writer.writerow([category, url])

    loop.stop()


def gather_images(loop, search):
    """
    search for images on ImageNet, write images to disk

    :param search: term to search ImageNet for
    :type search: str
    :param num_images: total number of images to download
    :type num_images: int
    """
    if isinstance(search, nltk.corpus.reader.wordnet.Synset):
        # get object name from synset
        search = search.name().split('.')[0].replace('_', ' ')

    # url format for search url
    search_url = search.replace(' ', '+').replace(',', '%2C').replace("'", "%27")
    # file format for file system
    search = search.replace(', ', '-').replace(' ', '_').replace("'", "")

    print(search_url)

    urls = get_image_urls(search_url)


    # for url in get_image_urls(search_url):
    #     loop.call_soon(build_collection, loop, url, search)

    # return urls


if __name__ == "__main__":
    main(DATA_DIR)