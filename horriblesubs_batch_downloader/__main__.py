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

import time

from docopt import docopt
from .scraper import Scraper
from .downloader import Downloader

def main():
    args = docopt(__doc__)
    print(args)

    # URL specified
    if args['<url>']:
        scraper = Scraper(url=args['<url>'])
    # Name specified
    elif args['<show_name>']:
        scraper = Scraper(show_name=args['<show_name>'])
        scraper.create_url_from_show_name()

    scraper.get_show_id()
    print("Found show id: {}".format(scraper.show_id))
    scraper.create_torrent_links(res=args['<res>'])

    # Range specified
    if args['<start>'] and args['<end>']:
        downloader = Downloader(links=scraper.fetch_episodes_in_range(int(args['<start>']), int(args['<end>'])))
    # Episode specified
    elif args['<episode>']:
        downloader = Downloader(links=scraper.fetch_episode(int(args['<episode>'])))
    # Fetch all
    else:
        downloader = Downloader(links=scraper.fetch_all_episodes())

    print("Found {} episodes! Downloading in 5 seconds, press CTRL-C to cancel.".format(len(downloader.links)))
    time.sleep(5)
    downloader.open_links()

if __name__ == "__main__":
    main()
