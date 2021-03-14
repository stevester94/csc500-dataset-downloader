#! /usr/bin/python3
import sys
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class StevesDownloader:
    def __init__(self, 
        finished_download_path,
        partial_download_path,
        log_path="./steves_downloader.log"):

        self.finished_download_path = finished_download_path
        self.partial_download_path  = partial_download_path

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options, service_args=["--log-path="+log_path])
        params = {'behavior': 'allow', 'downloadPath': self.partial_download_path}
        self.driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

        print ("Headless Chrome Initialized")
    
    def __del__(self):
        print("StevesDownloader destructing")
        self.driver.quit()

    def get_files_in_path(self, path):
        return os.listdir(path)

    def synchronous_download(self, url):

        starting_files = self.get_files_in_path(self.partial_download_path)

        if starting_files != []:
            raise Exception("Partial downloads was not empty, it needs to be empty. Time to freak out.")

        print("Beginning download")
        self.driver.get(url)

        while True:
            all_downloads_done = True
            current_files = self.get_files_in_path(self.partial_download_path)

            # Gotta wait for the download to start before we get to checking
            if current_files == []:
                continue 

            for f in current_files:
                if "crdownload" in f: 
                    all_downloads_done = False
                    break
            
            if all_downloads_done:
                break
            else:
                sleep(1)

        print("Download Finished")

        print("Moving files to completed downloads")

        for f in self.get_files_in_path(self.partial_download_path):
            src  = os.path.join(self.partial_download_path, f)
            dest = os.path.join(self.finished_download_path, f)

            if os.path.exists(dest):
                raise Exception("Destination of "+dest+" already exists. Time to freak out.")

            print("Move ", src, " => ", dest)

            os.rename(src, dest)
        print("Complete")



# Usage is <partial download path> <finished download path> <download list>
if __name__ == "__main__":
    download_urls = []
    with open(sys.argv[3], "r") as f:
        download_urls = [l.rstrip() for l in f]
    print("will download ", len(download_urls), " files")
    input("Press enter to continue ")
    downloader = StevesDownloader(partial_download_path=sys.argv[1], finished_download_path=sys.argv[2])

    for u in download_urls:
        downloader.synchronous_download(u)

    downloader=None
    sys.exit(0)