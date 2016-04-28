'''
Created on Apr 16, 2016

@author: shilpa
'''

from bs4 import BeautifulSoup
import requests
import re

LINE = re.compile('[^A-Za-z]')


def get_text(url):
    valid_lines = []
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError("Invalid URL.")
    soup = BeautifulSoup(r.text, "html.parser")
    # get poem
    poem = soup.find(id="poem")
    if poem is None:
        poem = soup.find(class_="poem")
    poem = poem.get_text('\n')
    poem = poem.split('\n')
    line_list = []
    for x in poem:
        x = str(x.encode('ascii', 'ignore')).strip()
        x = x + "  "
        if x.startswith('Source:'):
            break
        line_list.append(x)
    # delete blank lines
    for x in line_list:
        if not len(re.sub(LINE, "", x)) == 0:
            valid_lines.append(x)
    # get title
    title = soup.body.find('span', attrs={'class': 'hdg hdg_1'})
    title = title.get_text()
    title = str(title.encode('ascii', 'ignore')).strip()
    for x in valid_lines:
        print x
    return (title, valid_lines)


def main():
    pass


if __name__ == "__main__":
    get_text(
        "http://www.poetryfoundation.org/poems-and-poets/poems/detail/43644")
