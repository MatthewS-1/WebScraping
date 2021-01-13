# data preprocessing to get the entire text of the bible

import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.stewartonbibleschool.org/bible/text/index.html')
soup = BeautifulSoup(page.content, 'lxml')
unprocessed = soup.find_all("a", href=True)
links = []

# get each href that leads to a .txt file
for link in unprocessed:
    href = link.get("href")
    if href[-4:] == ".txt":
        links.append(href)


# processes each line of the bible and removes the location of each line
# example: "1:1 and _ said ..." would become "and _ said ..."
def process(string):
    seen = 0
    for i in range(len(string)):
        if string[i] == ":":
            seen += 1
        if seen == 2:
            return string[i + 2:]
    return ""


# go through each link we have and take the lines from it
file = open("bible.txt", "w") # store data in this file
for link in links:
    page = requests.get('http://www.stewartonbibleschool.org/bible/text/' + link)
    soup = BeautifulSoup(page.content, 'lxml')
    for lines in soup.find_all("p"):
        for line in lines.get_text().split("\n"):
            processed = process(line)
            if processed:
                file.write(process(line) + "\n")
