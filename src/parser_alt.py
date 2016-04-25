from bs4 import BeautifulSoup
import requests
import re


def get_text_alt(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError("Invalid URL.")
    soup = BeautifulSoup(r.text, "html.parser")
    poem_contents = soup.find_all(property="content:encoded")
    poem = poem_contents[0].get_text('\n')
    poem_raw = poem.split('\n')
    line_list = []
    for x in poem_raw:
        x = str(x.encode('ascii', 'ignore')).strip()
        line_list.append(x)
    for x in line_list:
        if x == "":
            line_list.remove(x)
    return line_list


def main():
    get_text("https://www.poets.org/poetsorg/poem/sun-bemidji-minnesota")


if __name__ == "__main__":
    main()
