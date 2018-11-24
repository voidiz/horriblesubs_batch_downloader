#!/usr/bin/env python3

import requests, re
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, show_name=None, url=None):
        self.show_name = show_name
        self.url = url
        self.show_id = None
        self.links = None

    def create_url_from_show_name(self):
        show_slug = re.sub(r" +", "-", self.show_name)
        self.url = "https://horriblesubs.info/shows/{}".format(show_slug)

    def get_show_id(self):
        r = requests.get(self.url)
        s = BeautifulSoup(r.text, 'lxml')
        id_obj = s.find(text=re.compile(r"var hs_showid = \d+;"))
        if not id_obj:
            raise ValueError("Couldn't find show id, most likely invalid URL/show name")
        self.show_id = re.search(r"\d+", id_obj).group(0)

    # Fetch all episodes with optional resolution, fetches
    # best possible resolution if specified resolution isn't found.
    def create_torrent_links(self, res=None):
        links = []
        next_id = 0
        api_url = "https://horriblesubs.info/api.php?method=getshows&type=show&showid={}&nextid={}".format(self.show_id, next_id)

        resolutions = ['1080', '720', '480', '360']
        selectors = {r:".link-{}p .hs-magnet-link a".format(r) for r in resolutions}
        resolutions.append('fallback')
        selectors['fallback'] = "[class^='rls-link link-'] .hs-magnet-link a"

        while requests.get(api_url).text != "DONE":
            s = BeautifulSoup(requests.get(api_url).text, 'lxml')
            for c in s.find_all(class_="rls-links-container"):

                # select specified resolution
                if res and res in resolutions:
                    if c.select(selectors[res]):
                        link = c.select(selectors[res])[0]

                    # select fallback if resolution isn't found
                    else:
                        link = c.select(selectors['fallback'])[-1]

                elif res and res not in resolutions:
                    raise ValueError("Invalid resolution, has to be {}.".format("/".join(resolutions[0:-1])))

                # select the highest quality
                else:
                    for r in resolutions:
                        if (c.select(selectors[r])):
                            # last matched item; usually the highest available resolution
                            link = c.select(selectors[r])[-1]
                            # print("found res: {}".format(r))
                            break
                links.append(link.get('href'))

            next_id += 1
            api_url = "https://horriblesubs.info/api.php?method=getshows&type=show&showid={}&nextid={}".format(self.show_id, next_id)

        self.links = links[::-1]

    def fetch_all_episodes(self):
        return self.links

    def fetch_episode(self, episode):
        if episode > len(self.links) or episode < 1:
            raise ValueError("Invalid episode number, please choose a number between 1 and {}".format(len(self.links)))
        return [self.links[episode-1]]

    def fetch_episodes_in_range(self, lower, upper):
        if upper > len(self.links) or lower < 1:
            raise ValueError("Invalid range, please specify a range between 1 and {}.".format(len(self.links)))
        return self.links[lower-1:upper]
