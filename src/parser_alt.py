from bs4 import BeautifulSoup
import requests
import re


def get_text(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError("Invalid URL.")
    soup = BeautifulSoup(r.text, "html.parser")
    poem = soup.find_all(class_="field-item even")
    poem = str(poem[3])
    poem = poem.replace('<br/>', '\n')
    poem = re.sub('<[^<]+?>', '', poem)
    poem_raw = poem.split('\n')
    line_list = []
    for x in poem_raw:
        x = str(x.encode('ascii', 'ignore')).strip()
        if x.startswith('Source:'):
            break
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
