import json
from re import compile as re_compile
from argparse import ArgumentParser
from requests import get
from bs4 import BeautifulSoup

MAGNET_REGEX_STR = r"magnet:\?xt=urn:(sha1|btih|ed2k|aich|kzhash|md5|tree:tiger):([A-Fa-f0-9]+|[A-Za-z2-7]+)(&amp;dn=([A-Za-z0-9!@#$%^:*<>,?\/()_+=.{}\{}\-])+)?(&amp;tr=([A-Za-z0-9!@#$%^:*<>,?\/()_+=.{}\{}\-]+))*"
MAGNET_REGEX = re_compile(MAGNET_REGEX_STR)
SEARCH_URL = "https://fitgirl-repacks.site/?s={}"


class SearchResult:
    def __init__(self, title: str, url: str):
        self.title = title
        self.urls = self.__get_magnet_links(url)

    def __get_magnet_links(self, url: str) -> list[str]:
        page = get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        magnets = soup.find_all("a", {"href": MAGNET_REGEX})
        return [magnet.get("href").replace("&amp;", "&") for magnet in magnets]

    def repr_json(self):
        return dict(title=self.title, urls=self.urls)


class Responses:
    def __init__(self, response: list[SearchResult]):
        self.response = response

    def repr_json(self):
        return dict(response=self.response)


class ResponseEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "repr_json"):
            return o.repr_json()
        return json.JSONEncoder.default(self, o)


def search_game(game_name: str) -> Responses:
    page = get(SEARCH_URL.format(game_name))
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="entry-title")
    ret: list[SearchResult] = []
    for result in results:
        title = result.find("a").get_text()
        link = result.find("a")["href"]
        ret.append(SearchResult(title, link))
    return Responses(ret)


parser = ArgumentParser()
parser.add_argument("game_name", type=str, help="Name of the game")
parser.add_argument(
    "dest",
    type=str,
    help="Destination path for results",
    default=".",
)

args = parser.parse_args()
game = args.game_name
dest = args.dest if args.dest.endswith("/") else f"{args.dest}/"
with open(f"{dest}results.json", "w") as f:
    f.write(json.dumps(search_game(game), cls=ResponseEncoder, indent=4))
