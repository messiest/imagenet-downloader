import os
import csv
import asyncio

import aiohttp

import tqdm

import numpy as np
import requests
from bs4 import BeautifulSoup
import nltk

def download_images(loop, image_dir, urls, category, n=100):  # TODO Move to async
    """
    download image from url to disk

    :param loop: event loop for the downloading.
    :type loop: asyncio.AbstractEventLoop()
    :param image_dir: key for the image file, used as the file name
    :type image_dir: str
    :param urls: urls for the image files
    :type urls: list
    :param category: categeory for the image, used to save to a class directory
    :type category: str
    :param n: number of pictures to download
    :type n: int
    :return: None
    :rtype: None
    """
    dir_path = os.path.join(image_dir, category)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    for url in urls:
        if len(os.listdir(dir_path)) >= n:
            break

        file_name = url.split('/')[-1]
        file_path = os.path.join(dir_path, file_name)
        try:
            image = requests.get(url, allow_redirects=False, timeout=2)
        except Exception as e:
            print(e)
            continue

        # print("{}/{} - {}: {}".format(  # TODO update to tqdm
        #     len(os.listdir(dir_path))+1,
        #     n,
        #     category,
        #     file_name
        # ))
        headers = image.headers
        if image.status_code != 200:
            print("\tCONNECTION ERROR {}: {}".format(image.status_code, url))
            # continue
        elif headers['Content-Type'] != 'image/jpeg':
            print("\tFILE TYPE ERROR {}: {}".format(headers['Content-Type'], url))
            # continue
        elif int(headers['Content-Length']) < 50000:  # only files > 50kb
            print("\tFILE SIZE ERROR {}: {}".format(headers['Content-Length'], url))
            # continue
        else:
            with open(file_path, 'wb') as file:
                file.write(image.content)  # download image

            write_to_file(file_path, image.content)

    loop.stop()  # escape loop iteration


def get_image_urls(wnid, shuffle=False):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """
    print("Fetching urls...")
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



# h/t https://gist.github.com/altipard/5d9735c446ddf7c2fcb8

# get content and write it to file
def write_to_file(filename, content):
    print("WRITING", filename)
    f = open(filename, 'wb')
    f.write(content)
    f.close()


# a helper coroutine to perform GET requests:
@asyncio.coroutine
def get(url):
    print("URL", url)
    # response = yield from aiohttp.request('GET', url)
    # return (yield from response.read_and_close())
    # try:
    image = requests.get(url, allow_redirects=False)
    return (yield from image.content)
    # except Exception as e:
    #     print(e)

    # headers = image.headers
    # if image.status_code != 200:
    #     print("\tCONNECTION ERROR {}: {}".format(image.status_code, url))
    # elif headers['Content-Type'] != 'image/jpeg':
    #     print("\tFILE TYPE ERROR {}: {}".format(headers['Content-Type'], url))
    # elif int(headers['Content-Length']) < 50000:  # only files > 50kb
    #     print("\tFILE SIZE ERROR {}: {}".format(headers['Content-Length'], url))
    # else:
    #     return (yield from image.content)
    # response = yield from requests.get(url, allow_redirects=False, timeout=2)
    # return (yield from response.content)


@asyncio.coroutine
def download_file(url):
    # this routine is protected by a semaphore
    # with (yield from r_semaphore):
    content = yield from asyncio.async(get(url))
    # create random filename
    length = 10
    file_name = url.split('/')[-1]
    file_path = os.path.join("images/", file_name)

    print(file_path)
    if content:
        write_to_file(file_path, content)

@asyncio.coroutine
def wait_with_progressbar(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


if __name__ == "__main__":
    print("HERE")

    images = get_image_urls(2084071)[:10]

    print(images)

    # avoid to many requests(coroutines) the same time.
    # limit them by setting semaphores (simultaneous requests)
    r_semaphore = asyncio.Semaphore(10)  # number of threads to run
    eloop = asyncio.get_event_loop()
    coroutines = [download_file(url) for url in images]
    # eloop.run_until_complete(asyncio.wait(coroutines))
    eloop.run_until_complete(wait_with_progressbar(coroutines))
    eloop.close()
