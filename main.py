import argparse
import multiprocessing as mp

from scraper import MetadataScraper, Downloader
from filesystem import prepare_folder

download_base_paths = [".", "data"]


def download(downloader):
    downloader.execute()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nhentai_no")
    parser.add_argument("-c", "--concurrent_count", metavar='n', type=int, default=20)

    args = parser.parse_args()

    nhentai_no = args.nhentai_no
    concurrent_count = args.concurrent_count

    print("Downloading gallery id#{}...".format(nhentai_no))
    meta_scraper = MetadataScraper(nhentai_no)
    metadata, link_generator = meta_scraper.get_info()
    if metadata and link_generator:
        print("Title: {}\t Pages: {}".format(metadata['title'], metadata['pages']))
        download_paths = download_base_paths + [metadata['title']]
        prepare_folder(download_paths)

        downloaders = [Downloader(page_link, download_paths) for page_link in link_generator]

        with mp.Pool(concurrent_count) as p:
            p.map(download, downloaders)

    else:
        print("no metadata is retrieved. exiting...")


if __name__ == "__main__":
    main()
