import requests
import re
from bs4 import BeautifulSoup

class Scraper():
    _resolutions = ['1080', '720', '480', '360']
    _base_api_url = "https://horriblesubs.info/api.php?method=getshows" + \
        "&type=show&showid={}&nextid={}"

    def __init__(self, show_name=None, url=None):
        self.show_name = show_name
        self.url = url
        self.show_id = None
        self.show_name = show_name
        self.links = []
        self.selectors = {}

        # Populate the selectors dict
        self.create_selectors()

    def create_selectors(self):
        """
        Create CSS selectors based on resolutions which are defined in the
        class.
        """

        for res in self._resolutions:
            if res == "fallback":
                selector = "[class^='rls-link link-'] .hs-magnet-link a"
            else:
                selector = ".link-{}p .hs-magnet-link a".format(res)
            
            self.selectors[res] = selector

    def create_url_from_show_name(self):
        """
        Create an url using the show name string.
        """

        show_slug = re.sub(r" +", "-", self.show_name)
        self.url = "https://horriblesubs.info/shows/{}".format(show_slug)

    def get_show(self):
        """
        Find the show id and show name using the url.
        """

        r = requests.get(self.url)
        s = BeautifulSoup(r.text, 'lxml')

        try:
            self.show_name = s.find(class_="entry-title").text
        except AttributeError:
            raise ValueError("Couldn't find the show using the given name/url")

        id_obj = s.find(text=re.compile(r"var hs_showid = \d+;"))
        if not id_obj:
            raise ValueError("Couldn't find show id, most likely invalid "
                             "URL/show name")
        self.show_id = re.search(r"\d+", id_obj).group(0)

    def create_torrent_links(self, res=""):
        """
        Fetch all episodes with optional resolution, fetches
        best possible resolution if specified resolution isn't found.
        """

        links = []
        next_id = 0
        api_url = self._base_api_url.format(self.show_id, next_id)

        while requests.get(api_url).text != "DONE":
            s = BeautifulSoup(requests.get(api_url).text, 'lxml')
            for c in s.find_all(class_="rls-links-container"):

                # Invalid resolution
                if res and res not in self._resolutions:
                    raise ValueError("Invalid resolution, has to be {}."
                                     .format("/".join(self._resolutions[0:-1])))

                # Select specified resolution
                if res and res in self._resolutions:
                    if c.select(self.selectors[res]):
                        # Select first item since select always returns
                        # a list
                        link = c.select(self.selectors[res])[0]

                    # Select fallback if resolution isn't found
                    else:
                        link = c.select(self.selectors['fallback'])[-1]

                # Select the highest quality
                else:
                    for r in self._resolutions:
                        if (c.select(self.selectors[r])):
                            # Last matched item is usually the highest
                            # available resolution
                            link = c.select(self.selectors[r])[-1]
                            break

                # Add the link
                links.append(link.get('href'))

            next_id += 1
            api_url = self._base_api_url.format(self.show_id, next_id)

        # Reverse the order since the parsing is done from the last episode
        # to the first episode.
        self.links = links[::-1]

    def fetch_all_episodes(self):
        """
        Fetch all episodes.
        """

        return self.links

    def fetch_episode(self, episode):
        """
        Fetch one episode.
        """

        if episode > len(self.links) or episode < 1:
            raise ValueError(
                "Invalid episode number, please choose a number between "
                "1 and {}".format(len(self.links)))
        return [self.links[episode-1]]

    def fetch_episodes_in_range(self, lower, upper):
        """
        Fetch a range of episodes.
        """

        if upper > len(self.links) or lower < 1:
            raise ValueError(
                "Invalid range, please specify a range between 1 and {}."
                .format(len(self.links)))
        return self.links[lower-1:upper]
