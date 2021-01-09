# Web Scraper for obtaining all coordinates for each USGS station
# USGS has a government database with lots of geographical data, so methods here could be expanded upon
# This was originally built for obtaining data for machine learning


import requests
from bs4 import BeautifulSoup
import json


# NOTE: some methods depend on data gathered from other methods. Ensure that they're run in the correct order.
def get_urls():  # gets the urls for each state's stations
    global urls
    urls = []
    page = requests.get("https://water.usgs.gov/osw/sediment/datasummary.html")
    soup = BeautifulSoup(page.content, 'html.parser')

    for tr in soup.find_all("tr")[5:-2]:
        try:
            urls.append("https://water.usgs.gov/osw/sediment/" + tr.findChildren()[1].get("href"))
        except:
            pass


def get_ids():  # gets the ids for each station in the USGS database
    ids_file = open("ids.txt", "w")
    ids = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        unprocessed = soup.find_all("tr")
        # count = 0
        for el in unprocessed[4:]:
            # count += 1 optional count variable for debugging
            id = el.findChildren()[1].text
            if id.isnumeric() and (len(id) == 15 or len(id) == 8):
                ids.append(id)
                ids_file.write(id + "\n")


ids = []
coords = {}


def get_coords():  # retrieves the coordinates for a station
    coords = {}
    for id in ids:
        # print(id)
        page = requests.get("https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=" + id)
        soup = BeautifulSoup(page.content, 'html.parser')
        lines = str(soup.get_text)
        lines = lines.split('\n')
        line = lines[-2].split('\t')
        coords[id] = " ".join(line[4:6])
    with open('coords.json', "w") as file:
        json.dump(coords, file)


def load_ids():
    global ids
    ids = []
    file = open("ids.txt", "r")
    for line in file:
        ids.append(line[:-1])


def load_coords():
    global coords
    with open('coords.json') as file:
        coords = json.load(file)


def main():
    # this will only work if all other methods have already obtained the data
    load_ids()
    load_coords()


if __name__ == '__main__':
    main()
