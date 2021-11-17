import requests
import re
from urllib.parse import urljoin

class Scanner:
    def __init__(self, url):
        self.target_url = url
        self.target_links = []
    
    def extract_links(self, url):
        response = requests.get(url)
        return re.findall('(?:href=*)(.*?)*', response.content)

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
            
        href_links = self.extract_links(url)
        for link in href_links:
            link = urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]
            
            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print(link)
                self.crawl(link)
#

