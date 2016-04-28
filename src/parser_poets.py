'''
Created on Apr 21, 2016

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
    poem_contents = soup.find_all(property="content:encoded")
    poem = poem_contents[0].get_text('\n')
    poem_raw = poem.split('\n')
    line_list = []
    for x in poem_raw:
        x = str(x.encode('ascii', 'ignore')).strip()
        x = x + "  "
        line_list.append(x)
    # delete blank lines
    for x in line_list:
        if not len(re.sub(LINE, "", x)) == 0:
            valid_lines.append(x)
    # get title
    title = soup.body.find('h1', attrs={'class': 'page__title title'})
    title = title.get_text()
    title = str(title.encode('ascii', 'ignore')).strip()
    return (title, valid_lines)


def main():
    get_text("https://www.poets.org/poetsorg/poem/epitaph-tyrant")


if __name__ == "__main__":
    main()
