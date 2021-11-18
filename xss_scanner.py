import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url):
        self.target_url = url
        self.session = requests.Session()
        self.pages_crawled = [url]

    def crawler(self, url=None):
        if url is None:
            url = self.target_url
        page = self.session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            if 'href' in link.attrs:
                if ':' not in link['href']:
                    new_link = url + link['href']
                    if new_link not in self.pages_crawled:
                        self.pages_crawled.append(new_link)
                        print("[FOUND] "+ new_link)
                        self.crawler(new_link)

    def extract_forms(self, url):
        response = self.session.get(url)

        parsed_html = BeautifulSoup(response.content, features="lxml")
        return parsed_html.findAll("form")

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
        return xss_script in response.text

    def xss_in_link(self, url):
        xss_script = "<Script>alert(\"Vulnerable\")</scripT>"
        url = url.replace("=", "=" + xss_script)
        response = self.session.get(url)
        return xss_script in response.text

    def run(self):
        self.crawler()

        for link in self.pages_crawled:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n\n[-->] Testing form in " + link)
                if self.xss_in_form(form, link):
                    print("[YAY] XSS discovered in " + link + " in the following form: ")
                    print(form)

            if "=" in link:
                print("\n\n[-->] Testing " + link)
                if self.xss_in_link(link):
                    print("[YAY] XSS discovered in " + link)
    


