import os
import argparse

from scraper import MetadataScraper, Downloader

download_base_paths = [".", "data"]


def construct_path(paths):
    work_paths = paths.copy()
    result = work_paths.pop(0)
    while work_paths:
        result = os.path.join(result, length_check(work_paths.pop(0).replace("/", "_")))
    return result


def length_check(path_elem):
    result = ""
    BYTE_LENGTH_LIMIT = 255
    CODEC = "utf-8"
    byte_length = len(path_elem.encode(CODEC))
    if byte_length > BYTE_LENGTH_LIMIT:
        i = BYTE_LENGTH_LIMIT
        while not result:
            try:
                result = path_elem.encode(CODEC)[:i].decode(CODEC)
            except UnicodeDecodeError:
                i = i - 1
                continue
    else:
        result = path_elem
    return result


def prepare_folder(paths):
    path = construct_path(paths)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("nhentai_no")

    args = parser.parse_args()

    nhentai_no = args.nhentai_no
    print("Downloading gallery id#{}...".format(nhentai_no))
    meta_scraper = MetadataScraper()
    metadata, image_generator = meta_scraper.get_info(nhentai_no)
    if metadata and image_generator:
        print("Title: {}\t Pages: {}".format(metadata['title'], metadata['pages']))
        download_paths = download_base_paths+[metadata['title']]
        prepare_folder(download_paths)

        for image_link, image in image_generator:
            path = construct_path(download_paths+[image_link.split("/")[-1]])
            downloader = Downloader(image_link, path)
            downloader.download()
            downloader.save()
    else:
        print("no metadata is retrieved. exiting...")