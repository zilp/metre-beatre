from bs4 import BeautifulSoup
import requests
import re


def get_text(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError("Invalid URL.")
    soup = BeautifulSoup(r.text, "html.parser")
    poem_contents = soup.find_all(property="content:encoded")
    poem = poem_contents[0].get_text('\n')
    print poem
    poem_raw = poem.split('\n')
    line_list = []
    for x in poem_raw:
        x = str(x.encode('ascii', 'ignore')).strip()
        line_list.append(x)
    for x in line_list:
        if x == "":
            line_list.remove(x)
    print line_list
    return line_list


def main():
    get_text("https://www.poets.org/poetsorg/poem/do-not-go-gentle-good-night")


if __name__ == "__main__":
    main()
