import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url):
        self.target_url = url
        self.target_links = []
        self.session = requests.Session()
    
    def extract_links(self, url):
        response = requests.get(url)
        return re.findall('(?:href=*)(.*?)*', response.content.decode('utf-8'))

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
                print("[FOUND] " + link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)

        parsed_html = BeautifulSoup(response.content)
        return parsed_html.findAll("forms")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
        method = form.get("method")

        input_lists = form.findAll("input")
        post_data = {}

        for input in input_lists:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")

            if input_type == "text":
                input_value = value
            
            post_data[input_name] = input_value

        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)

    def xss_in_form(self, form, url):
        xss_script = "<Script>alert(\"Vulnerable\")</scripT>"
        response = self.submit_form(form, xss_script, url)
        return xss_script in response.content

    def xss_in_link(self, url):
        xss_script = "<Script>alert(\"Vulnerable\")</scripT>"
        url = url.replace("=", "=" + xss_script)
        response = self.session.get(url)
        return xss_script in response.content

    def run(self):
        self.crawl()

        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n\n[-->] Testing form in " + link)
                if self.xss_in_form(form, link):
                    print("[YAY] XSS discovered in " + link + " in the following form: ")
                    print(form)

            if "=" in link:
                print("\n\n[-->] Testing " + link)
                if self.xss_in_form(link):
                    print("[YAY] XSS discovered in " + link)
    


