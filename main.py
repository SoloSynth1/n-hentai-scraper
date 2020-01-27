import os
import argparse

from metadatascraper import MetadataScraper, Downloader

download_base_paths = [".", "data"]


def construct_path(paths):
    work_paths = paths.copy()
    result = work_paths.pop(0)
    while work_paths:
        result = os.path.join(result, work_paths.pop(0).replace("/", "\/"))
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

    meta_scraper = MetadataScraper()
    metadata, image_generator = meta_scraper.get_info(args.nhentai_no)
    print("Title: {}\t Pages: {}".format(metadata['title'], metadata['pages']))
    download_paths = download_base_paths+[metadata['title']]
    prepare_folder(download_paths)

    for image_link, image in image_generator:
        path = construct_path(download_paths+[image_link.split("/")[-1]])
        downloader = Downloader(image_link, path)
        downloader.download()
        downloader.save()
