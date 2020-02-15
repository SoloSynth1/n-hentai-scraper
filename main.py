import argparse
import multiprocessing as mp

from scraper import MetadataScraper, Downloader
from filesystem import prepare_folder

download_base_paths = [".", "data"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nhentai_no")

    args = parser.parse_args()

    nhentai_no = args.nhentai_no
    print("Downloading gallery id#{}...".format(nhentai_no))
    meta_scraper = MetadataScraper(nhentai_no)
    metadata, link_generator = meta_scraper.get_info()
    if metadata and link_generator:
        print("Title: {}\t Pages: {}".format(metadata['title'], metadata['pages']))
        download_paths = download_base_paths + [metadata['title']]
        prepare_folder(download_paths)

        processes = []
        for page_link in link_generator:
            downloader = Downloader(page_link, download_paths)
            processes.append(mp.Process(target=downloader.execute))

        for process in processes:
            process.start()
        for process in processes:
            process.join()

    else:
        print("no metadata is retrieved. exiting...")


if __name__ == "__main__":
    main()
