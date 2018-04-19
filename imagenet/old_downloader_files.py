

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

        print("{}/{} - {}: {}".format(  # TODO update to tqdm
            len(os.listdir(dir_path))+1,
            n,
            category,
            file_name
        ))
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
