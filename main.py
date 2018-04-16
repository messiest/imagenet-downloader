import os
import argparse
import asyncio

from imagenet.downloader import get_image_urls


DATA_DIR = 'images/'


def main(item, data_dir=DATA_DIR):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    loop = asyncio.get_event_loop()  # async event loop
    gather_images(loop, item)
    loop.run_forever()  # execute queued work
    loop.close()  # shutdown loop


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "item",
        help="What image do you want to search for?",
        type=str,
    )
    args = parser.parse_args()
    item = args.item
    print("ITEM", item)
    main(item)

    # print(get_image_urls(item))
