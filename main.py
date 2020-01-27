import os
import argparse

from scraper import Scraper

download_base_paths = [".", "data"]

def save(image, paths):
    path = construct_path(paths)
    with open(path, 'wb') as f:
        f.write(image)
    print("\r{} saved".format(path), end="")

def construct_path(paths):
    work_paths = paths.copy()
    result = work_paths.pop(0)
    while work_paths:
        result = os.path.join(result, work_paths.pop(0))
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

    scraper = Scraper()
    metadata, image_generator = scraper.scrape(args.nhentai_no)
    print("Title: {}\t Pages: {}".format(metadata['title'], metadata['pages']))
    download_paths = download_base_paths+[metadata['title']]
    prepare_folder(download_paths)

    for image_link, image in image_generator:
        save(image, download_paths+[image_link.split("/")[-1]])
