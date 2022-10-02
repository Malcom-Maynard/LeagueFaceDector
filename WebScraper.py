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

    # Setting the name value if valid
    # returns:
    def set_name(self, name):

        if name.lower() in self.player_ID:
            self.name = name.lower()
            self._setUrl(self.name)

    # Checks if name value that is set is valid, if so it updates all the class values
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

    # returns the generated url to user
    # returns: str
    def get_url(self):
        return self.url

    # Returns in info from web scraping back to the user
    # returns:str,str,str,str
    def pull_infomation(self):

        # scrapes the saved url and saves in data.html
        scraper = cloudscraper.create_scraper()
        r = scraper.get(self.url).text
        soup = BeautifulSoup(r, "html.parser")
        with open("data.html", "w", encoding="utf-8") as file:
            file.write(str(soup))

        # setting  values for rank and lp given in the state of the page
        try:
            rank = soup.find("div", {"class": "tier"}).getText()
            lp = soup.find("div", {"class": "lp"}).getText()
        except:
            rank = "unranked"
            lp = "0"

        message = ""

        choices = {
            "iron": "Yikes",
            "bronze": "Could be better",
            "sliver": "eyy?",
            "gold": "Nice job",
            "diamond": "Wow there buddy",
            "master": "Wet napkin",
            "unranked": "Sane human",
        }
        message = choices.get(rank.lower(), "default")

        return rank, lp, self.player_ID[self.name][1], message
