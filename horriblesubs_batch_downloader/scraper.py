import requests, re
from bs4 import BeautifulSoup

"""
https://horriblesubs.info/shows/
https://horriblesubs.info/api.php?method=getshows&type=show&showid=476&nextid=0
"""

class Scraper():
    def __init__(self, show_name=None, url=None):
        self.show_name = show_name
        self.url = url
        self.show_id = None
        self.links = None

    def create_url_from_show_name(self):
        self.url = "https://horriblesubs.info/shows/{}".format(self.show_name)

    def get_show_id(self):
        r = requests.get(self.url)
        s = BeautifulSoup(r.text, 'lxml')
        id_obj = s.find(text=re.compile(r"var hs_showid = \d+;"))
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
                if res and res in resolutions and c.select(selectors[res]): # specified resolution
                    if c.select(selectors[res]):
                        links += c.select(selectors[res])
                    else: # fallback if resolution isn't found
                        links += c.select(selectors['fallback'])
                elif res is None: # highest quality
                    for r in resolutions:
                        if (c.select(selectors[r]) and r != 'fallback'):
                            links += c.select(selectors[r])
                            print("found res: {}".format(r))
                            break
                        elif (r == 'fallback'):
                            links += c.select(selectors[r])[-1] # last matched item; usually the highest available resolution
                            print("found res: {}".format(r))
                            break
            next_id += 1
            api_url = "https://horriblesubs.info/api.php?method=getshows&type=show&showid={}&nextid={}".format(self.show_id, next_id)

        self.links = links[::-1]

    def fetch_episodes_in_range(self):
        pass

# testing
test = Scraper(url="https://horriblesubs.info/shows/k")
test.get_show_id()
print(test.show_id)
test.create_torrent_links()
print(test.links)
asdfk = {l:n for l,n in enumerate(test.links)}
print(asdfk)

