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


# This gets the links that are represented as the little curvy box with "Zip File" or "Text Document" in it
class StevesDownloadFinder(HTMLParser):
    def __init__(self, base_url):
        super().__init__()

        self.urls = []
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for a in attrs:
                if a[0] == "title" and a[1] == "Zip File":
                    for a in attrs:
                        if a[0] == "href":
                            self.urls.extend( [self.base_url + a[1],] )
                elif a[0] == "title" and a[1] == "Text Document":
                    for a in attrs:
                        if a[0] == "href":
                            self.urls.extend( [self.base_url + a[1],] )


    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def get_urls(self):
        # There's another anchor element that has the download path. I'm too lazy to disambiguate so just get the uniques
        return list(set(self.urls))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Got: ", sys.argv, file=sys.stderr)
        raise Exception("Usage is: URL of collection of downloads")

    r = requests.get(sys.argv[1] + hack_to_get_all_items_in_collection)

    if r.status_code != 200:
        raise Exception("Fetching single collection URL failed")

    download_finder = StevesDownloadFinder(ultra_base_url)
    download_finder.feed(r.text)

    download_urls = download_finder.get_urls()

    # All bets are off, found some IQ snapshots with 2 files attached (Though luckily they had the same sha)
    # if len(download_urls) % 2 != 0:
    #     pprint(download_urls)
    #     raise Exception("Got ", len(download_urls), " urls to download. Expected an even number. Offending url: ", sys.argv[1])

    for d in download_urls:
        print(d)