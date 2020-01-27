import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self):
        self.sess = requests.session()
        self.url = "https://nhentai.net/g/{}"
        self.nhentai_no = None


    def scrape(self, nhentai_no):
        self.nhentai_no = nhentai_no
        try:
            self.metadata = self.get_gallery_metadata()
            self.page_links = self.construct_page_links()
            print("metadata retrieved sucessfully")
            return self.metadata, self.create_image_generator()
        except Exception as e:
            print("exception occurred when retrieving metadata.")
            return False

    def create_image_generator(self):
        for page_link in self.page_links:
            image_link = self.get_image_link(page_link)
            yield image_link, self.download(image_link)


    def get_gallery_metadata(self):
        metadata = {}
        response = self.sess.get(self.url.format(self.nhentai_no), headers=None)
        soup = BeautifulSoup(response.text, 'lxml')
        info = soup.find(id="info")
        metadata["title"] = info.find('h2').text
        metadata["pages"] = int([x.text for x in info.find_all('div') if ' pages' in x.text][0].split(' ')[0])
        return metadata

    def construct_page_links(self):
        page_links = [self.url.format(self.nhentai_no) + "/{}".format(i + 1) for i in range(self.metadata['pages'])]
        return page_links

    def get_image_link(self, page_link):
        response = self.sess.get(page_link)
        soup = BeautifulSoup(response.text, 'lxml')
        image_container = soup.find(id="image-container")
        image_link = image_container.find('img')['src']
        return image_link

    def download(self, image_link):
        response = self.sess.get(image_link)
        if response.status_code < 400:
            image = response.content
            return image
        else:
            print("failed to download image")
            return None