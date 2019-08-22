import scrapy
import requests
import os
import subprocess
import json
import unittest

class NewSpider(scrapy.Spider):

    name = "new_spider"

    start_urls = ['http://172.18.58.238/creative/']

    def parse(self, response):
        yield {'Referene Webpage': response.text}

        xpath_selector = '//img'

        for x in response.xpath(xpath_selector):

            newsel = '@src'

            image = x.xpath(newsel).extract_first()
            if ".jpg" in image:
                yield {
                    'Image Link': x.xpath(newsel).extract_first()
                }
            else:
                continue


url = "http://172.18.58.238/creative/"
r = requests.get(url)
print(r.text)

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

url2 = 'http://httpbin.org/headers'
rh = requests.get(url2, headers=headers)
print(rh.text)


class TestDA_Group10(unittest.TestCase):

    def test_status(self):
        self.assertEqual(r.status_code, 200)

    def test_user(self):
        self.assertEqual(headers,{'User-Agent': 'Mobile'})

    def test_scrappy_jpg(self):
        if os.path.exists('./Group10results.json'):
            os.remove('./Group10results.json')
        subprocess.Popen(['scrapy', 'runspider', 'DA_Group10.py', '-o', 'Group10results.json', '-t', 'json']).wait()
        results_file = open('Group10results.json', 'r')
        scrappy_output = json.load(results_file)
        results_file.close()
        for entries in scrappy_output:
            for key in entries.keys():
                if key == 'Image Link':
                    self.assertTrue(str(entries[key]).endswith('jpg'))

if __name__ == '__main__':
    unittest.main()

