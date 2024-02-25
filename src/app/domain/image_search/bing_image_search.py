# mypy: ignore-errors
# ruff: noqa

# adapted from code by @stephenhouser on github
# https://gist.github.com/stephenhouser/c5e2b921c3770ed47eb3b75efbc94799
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), "html.parser")


def bing_image_search(query):
    query = query.split()
    # query.pop()
    query = "+".join(query)
    # query.split()
    url = "http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    # add the directory for your image here
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url, header)
    image_result_raw = soup.find("a", {"class": "iusc"})

    m = json.loads(image_result_raw["m"])
    murl, turl = m["murl"], m["turl"]  # mobile image, desktop image

    image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
    return (image_name, murl, turl)


if __name__ == "__main__":
    query = sys.argv[1]
    results = bing_image_search(query)
    print(results)
