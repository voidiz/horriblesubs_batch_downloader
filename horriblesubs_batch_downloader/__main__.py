#!/usr/bin/env python3

"""Horriblesubs Batch Downloader

Usage:
    hsbd <url> (-a | <episode> | (<start> <end>)) [-r <res>]
    hsbd -n <show_name> (-a | <episode> | (<start> <end>)) [-r <res>]
    hsbd -h | --help

Examples:
    # Download all episodes in the highest quality from a url:
    hsbd "https://horriblesubs.info/shows/kuzu-no-honkai" -a

    # Download episodes 1 through 5 in 720p using a show name:
    hsbd -n "Kuzu no Honkai" 1 5 -r 720

Options:
    -h, --help          Show this screen.
    -a, --all           Download all episodes.
    -n, --name          Specify show by name.
    -r, --resolution    Specify resolution (1080, 720, 480, 360).

"""

import time

from docopt import docopt
from horriblesubs_batch_downloader.scraper import Scraper
from horriblesubs_batch_downloader.link_handler import LinkHandler


def main():
    args = docopt(__doc__)

    # URL specified
    if args['<url>']:
        scraper = Scraper(url=args['<url>'])

    # Name specified
    elif args['<show_name>']:
        scraper = Scraper(show_name=args['<show_name>'])
        scraper.create_url_from_show_name()

    scraper.get_show()
    print("Found show '{}' with id {}".format(scraper.show_name,
                                              scraper.show_id))
    scraper.create_torrent_links(res=args['<res>'])

    # Range specified
    if args['<start>'] and args['<end>']:
        links = scraper.fetch_episodes_in_range(int(args['<start>']),
                                                int(args['<end>']))

    # Episode specified
    elif args['<episode>']:
        links = scraper.fetch_episode(int(args['<episode>']))

    # Fetch all
    else:
        links = scraper.fetch_all_episodes()

    linkHandler = LinkHandler(links)

    print("Found {} episodes! Downloading in 5 seconds, press CTRL-C "
          "to cancel.".format(len(links)))
    time.sleep(5)
    linkHandler.open_links()


if __name__ == "__main__":
    main()
