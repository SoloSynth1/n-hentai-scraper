import time
import requests
from bs4 import BeautifulSoup


class Requester:

    def __init__(self):
        self.POLITENESS = 3
        self.TIMEOUT = 10
        self.sess = requests.session()
        self.response = None

    def retry(self):
        print("Retrying...")
        time.sleep(self.POLITENESS)

    def get(self, url, check_content_length=False):
        print("Requesting {}...".format(url))
        while True:
            try:
                self.response = self.sess.get(url, timeout=self.TIMEOUT)
                if self.response_is_valid(check_content_length):
                    break
            except:
                pass
            self.response = None
            self.retry()
        print("Valid response received.")

    def response_is_valid(self, check_content_length=False):
        assert self.response
        if self.response.status_code == 200:
            headers = self.response.headers
            content = self.response.content
            if "Content-Length" in headers.keys():
                content_length = int(headers["Content-Length"])
                actual_content_length = len(content)
                print("Reported content length: {}, Actual content length: {}".format(content_length, actual_content_length))
                if content_length == actual_content_length:
                    print("Response is OK")
                    return True
                else:
                    print("content length not matching")
            else:
                print("Header doesn't contain content length information.")
                if check_content_length:
                    print("Assuming bad response...")
                    return False
                else:
                    print("Assuming good response...")
                    return True
        return False


class MetadataScraper(Requester):

    def __init__(self, nhentai_no):
        super().__init__()
        self.url = "https://nhentai.net/g/{}".format(nhentai_no)

    def get_info(self):
        try:
            self.metadata = self.get_gallery_metadata()
            self.page_links = self.construct_page_links()
            print("metadata retrieved sucessfully")
            return self.metadata, self.create_image_generator()
        except Exception as e:
            print("exception occurred when retrieving metadata.")
            print("error info: {}".format(e))
            return None, None

    def create_image_generator(self):
        for page_link in self.page_links:
            image_link = self.get_image_link(page_link)
            yield image_link

    def get_gallery_metadata(self):
        metadata = {}
        self.get(self.url, check_content_length=False)
        soup = BeautifulSoup(self.response.text, 'lxml')
        info = soup.find(id="info")
        title_jp = info.find('h2')
        title_en = info.find('h1')
        if title_jp:
            metadata["title"] = title_jp.text
        else:
            metadata["title"] = title_en.text
        metadata["pages"] = int([x.text for x in info.find_all('div') if ' pages' in x.text][0].split(' ')[0])
        return metadata

    def construct_page_links(self):
        page_links = [self.url + "/{}".format(i + 1) for i in range(self.metadata['pages'])]
        return page_links

    def get_image_link(self, page_link):
        self.get(page_link)
        soup = BeautifulSoup(self.response.text, 'lxml')
        image_container = soup.find(id="image-container")
        image_link = image_container.find('img')['src']
        return image_link


class Downloader(Requester):

    def __init__(self, image_link, target_path):
        super().__init__()
        self.image_link = image_link
        self.target_path = target_path
        self.image = None
        self.TIMEOUT = 10

    def download(self):
        print("Downloading {}...".format(self.image_link))
        self.get(self.image_link, check_content_length=True)
        self.image = self.response.content
        print("Download Complete.")

    def save(self):
        print("Saving image to {}...".format(self.target_path), end="")
        with open(self.target_path, 'wb') as f:
            f.write(self.image)
        print("Done.")
