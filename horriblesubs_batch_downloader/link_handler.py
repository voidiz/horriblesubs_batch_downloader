import sys
import subprocess
import os

from horriblesubs_batch_downloader.rd_client import RDClient


class LinkHandler():
    def __init__(self, links):
        self.links = links

    def open_links(self):
        """ Open all links passed to the downloader. """

        for link in self.links:
            self.open_link(link)

    def add_to_rd(self, api_token):
        """
        Add all links to RealDebrid.
        """

        rdClient = RDClient(api_token)

        for link in self.links:
            res = rdClient.add_magnet(link)
            print("Added", res["id"])
            print("Started {} with status code {}".format(
                res["id"], rdClient.select_files(res["id"])))
        
        print("Done! Finished adding and starting all torrents to RD.")

    @staticmethod
    def open_link(link):
        """ Open a single link. """

        if sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", link], stdout=subprocess.DEVNULL)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", link], stdout=subprocess.DEVNULL)
        elif sys.platform.startswith("win32"):
            os.startfile(link)
        else:
            subprocess.Popen(["xdg-open", link], stdout=subprocess.DEVNULL)
