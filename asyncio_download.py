#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Daniel Altiparmak (sixfinger78@gmail.com)"
__copyright__ = "Copyright (C) 2015 Daniel Altiparmak"
__license__ = "GPL 3.0"


import asyncio
import aiohttp
import tqdm

import string
import random

# get content and write it to file
def write_to_file(filename, content):
    f = open(filename, 'wb')
    f.write(content)
    f.close()

# a helper coroutine to perform GET requests:
@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read_and_close())


@asyncio.coroutine
def download_file(url):
    # this routine is protected by a semaphore
    with (yield from r_semaphore):
        content = yield from asyncio.async(get(url))

        # create random filename
        length = 10
        file_string = ''.join(random.choice(
            string.ascii_lowercase + string.digits) for _ in range(length)
                              )
        filename = '{}.png'.format(file_string)

        write_to_file(filename, content)

'''
make nice progressbar
install it by using `pip install tqdm`
'''
@asyncio.coroutine
def wait_with_progressbar(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


images = ['http://lorempixel.com/1920/1920/' for i in range(100)]


# avoid to many requests(coroutines) the same time.
# limit them by setting semaphores (simultaneous requests)
r_semaphore = asyncio.Semaphore(10)

coroutines = [download_file(url) for url in images]
eloop = asyncio.get_event_loop()
#eloop.run_until_complete(asyncio.wait(coroutines))
eloop.run_until_complete(wait_with_progressbar(coroutines))
eloop.close()
