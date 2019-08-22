import scrapy
import requests
import unittest
import Browser
import subprocess
import os
import json


class NewSpider(scrapy.Spider):
    name = "new_spider"

    start_urls = ['http://172.18.58.238/photography/']


    def parse(self, response):
        # save out the reference webpage code
        yield {'Referene Webpage': response.text}

        # Image selector
        xpath_selector = '//img'
        for x in response.xpath(xpath_selector):
            newsel = '@src'

            img_link = x.xpath(newsel).extract_first()

            if img_link.endswith('.jpg') or img_link.endswith('.jpeg'):
                yield {
                    'Image Link': img_link
                }
                #the IF is only save jpg relevant pictures, dh other thing
                #yield = generate output
        # Recursively search through all page links for images on those links
        page_selector = '.next a ::attr(href)'
        next_page = response.css(page_selector).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )



url = "http://172.18.58.238/photography/"

r = requests.get(url)

print("Status code:")
print("\t *", r.status_code)

h = requests.head(url)
print("Header:")
print("**********")

for x in h.headers:
    print("\t ", x, ":", h.headers[x])
print("**********")

headers = {
    'User-Agent': "Mobile"
}

r = requests.get(url)

url2 = 'http://httpbin.org/headers'
rh = requests.get(url2, headers=headers)
print(rh.text)




class TestBrowser(unittest.TestCase):

    def test_status(self):
        self.assertTrue(Browser.r.status_code == 200) #assert true is to double cfm the server will reply ok

    def test_user_agent(self):
        header_dict = eval(Browser.rh.text)
        self.assertTrue(header_dict['headers']['User-Agent'] == 'Mobile')

    def test_scrappy_jpg(self):
        if os.path.exists('./results.json'):
            os.remove('./results.json')
        subprocess.Popen(['scrapy', 'runspider', 'Scrapy.py', '-o', 'results.json', '-t', 'json']).wait() #run scrapy script 10c
        results_file = open('results.json', 'r') #produce json file
        scrappy_output = json.load(results_file)
        results_file.close()
        for entries in scrappy_output:
            for key in entries.keys():
                if key == 'Image Link': #jpg
                    self.assertTrue(str(entries[key]).endswith('jpg') or str(entries[key]).endswith('jpeg'))  #makesure extract jpg file



if __name__ == '__main__':
    unittest.main()