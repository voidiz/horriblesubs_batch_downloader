#!/usr/bin/env python3

"""Horriblesubs Batch Downloader

Usage:
    horriblesubs_batch_downloader 

"""

from docopt import docopt
from .scraper import Scraper
from .downloader import Downloader

def main():
    url = input("Input url: ")
    scraper = Scraper(url=url)
    scraper.get_show_id()
    scraper.create_torrent_links()
    downloader = Downloader(links=scraper.fetch_all_episodes())
    downloader.open_links()

if __name__ == "__main__":
    main()
