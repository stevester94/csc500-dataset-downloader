# Description
This is a collection of utility scripts to make it easy to download bulk files from Northeastern University's library (Which is where Al Shawabka et. al. dataset resides)

# Motivation
NEU library's data repository services are slow, and error prone. I've had multiple downloads stall, queueing too many files results in files being ommited from the zipped download, and the zipping process takes ages. I have found it easier to just write scripts to scrape the website and download each file manually.

# Pieces and their purpose
## collection_finder.py
Finds all collections on a NEU page

## download_finder.py
Finds all downloads on a NEU page

## get_downloads.bash
Ties collection_finder.py and download_finder.py together to get all the download links for a given experiment.

## steves_downloader.py
Uses selenium and headless chrome to actually download the links. Note that this is likely overngineered but it's what I came up with and it worked.

## download_it_all.bash
Calls steves_downloader with all the downloads obtained from get_downloads.bash

## openssl.cnf
NEU's library uses some sort of weak cipher which the standard ssl config does not like. `export OPENSSL_CONF=$(realpath openssl.cnf)` allows tools like curl and python requests to fetch their pages.

# CONOPS
Note that this is from memory and so may not be exact
```bash
# Get all the download links for their in the wild experiment and save it to all_downloads
./get_downloads.bash > all_downloads

# Creates pre-requisite dirs and then downloads sequentially (It's gonna take a while)
./download_it_all.bash
```

# Installing selenium and headless Chrome
(Note this is on Ubuntu 20.04 )

```bash
##############
# Install chrome
# (I have version 87.0.4280.141 (Official Build) (64-bit))
##############

# Unknown if this is needed
sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4

##############
# Installed chromedriver  Starting ChromeDriver 87.0.4280.88
# I installed this from their website
##############

pip3 install selenium
```