# TODO

import cfscrape

scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
print(scraper.get("https://nhentai.net/g/177014/").content)  # => "<!DOCTYPE html><html><head>..."