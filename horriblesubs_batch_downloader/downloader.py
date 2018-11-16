#!/usr/bin/env python3

import sys, subprocess, os

class Downloader():
    def __init__(self, links):
        self.links = links

    # Open all links passed to the downloader
    def open_links(self):
        for link in self.links:
            if sys.platform.startswith("linux"):
                subprocess.Popen(["xdg-open", link], stdout=subprocess.DEVNULL)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", link], stdout=subprocess.DEVNULL)
            elif sys.platform.startswith("win32"):
                os.startfile(link)
            else:
                subprocess.Popen(["xdg-open", link], stdout=subprocess.DEVNULL)
