import argparse
import multiprocessing as mp

from scraper import MetadataScraper, Downloader
from filesystem import prepare_folder

download_base_paths = [".", "data"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nhentai_no")
    parser.add_argument("-c", metavar='THREAD_COUNT', type=int, default=10)

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

        downloader_args = []
        for page_link in link_generator:
            downloader_args.append((page_link, download_paths))

        with mp.Pool(concurrent_count) as p:
            p.starmap(Downloader, downloader_args)

    else:
        print("no metadata is retrieved. exiting...")


if __name__ == "__main__":
    main()
