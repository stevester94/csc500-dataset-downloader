#! /usr/bin/python3

import requests
import sys
import json

from html.parser import HTMLParser

import pprint
pp = pprint.PrettyPrinter(indent=4)
pprint = pp.pprint

ultra_base_url = "https://repository.library.northeastern.edu/"

hack_to_get_all_items_in_collection='?utf8=✓&sort=title_ssi+asc&per_page=100&id=neu%3Agm80kf51n&rows=10'


# Will print the URLs of all the collections on a page.
# Chain this program repeatedly until you get to the base case of no more collections
# At that point you will use the download finder
class StevesCollectionFinder(HTMLParser):
    def __init__(self, base_url):
        super().__init__()

        self.urls = []
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            for a in attrs:
                if a[0] == "data-href":
                    self.urls.extend( [self.base_url + a[1],] )

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def get_urls(self):
        return self.urls

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Got: ", sys.argv, file=sys.stderr)
        raise Exception("Usage is: URL of collection of collections (IE, a listing of devices)")
    collection_finder = StevesCollectionFinder(ultra_base_url)

    r = requests.get(sys.argv[1]+hack_to_get_all_items_in_collection)

    if r.status_code != 200:
        raise Exception("Fetching collections URL failed")
    collection_finder.feed(r.text)

    collection_urls = collection_finder.get_urls()

    for c in collection_urls:
        print(c)