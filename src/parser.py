from bs4 import BeautifulSoup
import requests

def get_text(url):
    r = requests.get(url)
    if r.status_code == 404:
        raise ValueError("Invalid URL.")
    soup = BeautifulSoup(r.text, "html.parser")
    poem = soup.find(id="poem")
    if poem is None:
        poem = soup.find(class_="poem")
    poem = poem.get_text('\n')
    poem = poem.split('\n')
    line_list = []
    for x in poem:
        x = str(x.encode('ascii', 'ignore')).strip()
        if x.startswith('Source:'):
            break
        line_list.append(x)
    return line_list


def main():
    pass


if __name__ == "__main__":
    get_text("http://www.poetryfoundation.org/poems-and-poets/poems/detail/89189")
