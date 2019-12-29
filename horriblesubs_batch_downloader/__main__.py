#!/usr/bin/env python3

"""Horriblesubs Batch Downloader

Usage:
    hsbd <url> (-a | <episode> | (<start> <end>))
               [-r <res>] [--add-to-rd]
    hsbd -n <show_name> (-a | <episode> | (<start> <end>))
               [-r <res>] [--add-to-rd]
    hsbd --set-rd-token
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
    --add-to-rd         Add the magnet links to RealDebrid.
    --set-rd-token      Set RealDebrid API token.

"""

import time

from docopt import docopt
from horriblesubs_batch_downloader.scraper import Scraper
from horriblesubs_batch_downloader.link_handler import LinkHandler
from horriblesubs_batch_downloader.config import Config


def main():
    args = docopt(__doc__)
    config = Config()

    if args['--set-rd-token']:
        config.set_rd_api_token()
        return

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

    print("Found {} episodes!".format(len(links)))

    # Add links to RD
    if args['--add-to-rd']:
        api_token = config.get_rd_api_token()
        print("Adding links to RealDebrid")
        linkHandler.add_to_rd(api_token)
        return

    # Download with torrent client
    print("Downloading in 5 seconds, press CTRL-C to cancel.")
    time.sleep(5)
    linkHandler.open_links()


if __name__ == "__main__":
    main()
