'''
Created on Apr 21, 2016

@author: shilpa
'''


from bs4 import BeautifulSoup
import requests
import re


def get_text_alt(url):
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
    for x in line_list:
        if x == "":
            line_list.remove(x)
    # get title
    title = soup.body.find('h1', attrs={'class': 'page__title title'})
    title = title.get_text()
    return (title, line_list)


def main():
    get_text_alt("https://www.poets.org/poetsorg/poem/do-not-go-gentle-good-night")


if __name__ == "__main__":
    main()
