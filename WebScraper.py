from copy import deepcopy
from select import select
from urllib.error import URLError
import requests
import cloudscraper
import json
from bs4 import BeautifulSoup


class WebScraper:
    url = "https://na.op.gg/summoners/NA/OmegaOmori"
    player_ID = {
        "amari": ["NA", "kidTeemo77"],
        "jankos": ["EUW", "G2BOOMER"],
        "spica": ["NA", "ASTROBOY99"],
    }
    name = "amari"

    def __init__(self, name="amari"):

        self._setUrl(name.lower())

    def set_name(self, name):
        print(name.lower())
        print(name.lower() in self.player_ID)
        if name.lower() in self.player_ID:
            self.name = name.lower()
            self._setUrl(name.lower())

    def _setUrl(self, name):
        if type(name) == str:
            print(name.lower() in self.player_ID)
            if name.lower() in self.player_ID:
                self.name = name.lower()
                region = self.player_ID[name][0]
                summoner_name = self.player_ID[name][1]
                self.url = (
                    "https://"
                    + region
                    + ".op.gg/summoners/"
                    + region
                    + "/"
                    + summoner_name
                )

    def get_url(self):
        return self.url

    def pull_infomation(self):
        # html_text = requests.get(self.url, "lxml").text
        print(self.url)
        scraper = cloudscraper.create_scraper()
        r = scraper.get(self.url).text
        soup = BeautifulSoup(r, "html.parser")
        with open("data.html", "w", encoding="utf-8") as file:
            file.write(str(soup))

        try:
            rank = soup.find("div", {"class": "tier"}).getText()
            lp = soup.find("div", {"class": "lp"}).getText()
        except:
            rank = "unranked"
            lp = "0"
        print(rank)
        print(lp)
        message = ""

        choices = {
            "iron": "Negative ass",
            "bronze": "Whore *spits*",
            "sliver": "No bitches",
            "gold": "No bitches^2",
            "Diamond": "Fatherless...",
            "Master": "Wet napkin",
            "unranked": "Sane human",
        }
        message = choices.get(rank.lower(), "default")

        return rank, lp, self.player_ID[self.name][1], message
