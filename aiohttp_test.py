import aiohttp
import asyncio
import async_timeout

from wordnet.utils import get_wnid
# from imagenet.downloader import get_image_urls


async def get_image_urls(wnid, shuffle=False):
    """
    return image urls from https://www.image-net.org

    :param search_item: WNID to search for
    :type search_item: str
    """
    image_urls = []

    # image net search id
    api_url = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n0{}"
    url = api_url.format(wnid)
    html = requests.get(url)  # html for search
    urls = (image_url for image_url in html.text.split('\r\n') if image_url)
    image_urls = [url.split()[1] for url in urls if url != '\n']

    if shuffle:
        np.random.shuffle(image_urls)  # randomize order

    return await image_urls


def parse_urls(html, shuffle=False):
    urls = (image_url for image_url in html.text.split('\r\n') if image_url)
    image_urls = [url.split()[1] for url in urls if url != '\n']

    if shuffle:
        np.random.shuffle(image_urls)  # randomize order

    return image_urls


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            # return await response.text()
            html = response.text()
            # urls = [image_url for image_url in html.text.split('\r\n') if image_url]
            return await html

async def main():
    term = get_wnid('bat')
    api_url = "http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n0{}".format(term)
    async with aiohttp.ClientSession() as session:
        html = await parse_urls(fetch(session, api_url))
        print(html)


@asyncio.coroutine
def wait_with_progressbar(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f

loop = asyncio.get_event_loop()

# coroutines = [download_file(url) for url in images]


# eloop.run_until_complete(wait_with_progressbar(coroutines))
# loop.run_until_complete(wait_with_progressbar(main('dog')))
loop.run_until_complete(main())
