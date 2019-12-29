import sys, subprocess, os

class LinkHandler():
    def __init__(self, links):
        self.links = links

    def open_links(self):
        """ Open all links passed to the downloader. """

        for link in self.links:
            self.open_link(link)
    
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
