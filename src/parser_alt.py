from bs4 import BeautifulSoup
import requests

def get_text(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError("Invalid URL.")
    soup = BeautifulSoup(r.text, "html.parser")
    poem = soup.find_all(class_="field-item even")
    poem = poem[3].getText()
    # poem_text = str(poem.get_text('\n'))
    poem_raw = poem.split('\n')
    line_list = []
    for x in poem_raw:
        x = str(x.encode('ascii', 'ignore')).strip()
        if x.startswith('Source:'):
            break
        line_list.append(x)
    for x in line_list:
        print x
    return line_list


def main():
    get_text("https://www.poets.org/poetsorg/poem/do-not-go-gentle-good-night")


if __name__ == "__main__":
    main()
