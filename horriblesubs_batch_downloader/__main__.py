#!/usr/bin/env python3

"""Horriblesubs Batch Downloader

Usage:
    horriblesubs_batch_downloader <url> (-a | <episode> | (<start> <end>)) [-r <res>]
    horriblesubs_batch_downloader -n <show_name> (-a | <episode> | (<start> <end>)) [-r <res>]
    horriblesubs_batch_downloader -h | --help

Examples:
    # Download all episodes in the highest quality from a url:
    horriblesubs_batch_downloader "https://horriblesubs.info/shows/kuzu-no-honkai" -a

    # Download episodes 1 through 5 in 720p using a show name:
    horriblesubs_batch_downloader -n "Kuzu no Honkai" 1 5 -r 720


Options:
    -h, --help          Show this screen.
    -a, --all           Download all episodes.
    -n, --name          Specify show by name.
    -r, --resolution    Specify resolution (1080, 720, 480, 360).

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
