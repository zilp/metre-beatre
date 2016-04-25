'''
Created on Apr 24, 2016

@author: shilpa
'''
from parser import get_text
import parser, parser_alt, analyzeMeter, rhyme

# used by server
def main(url):
    poem = []
    if "poets.org" in url:
        poem = parser_alt.get_text_alt(url)
    elif "poetryfoundation" in url:
        poem = parser.get_text(url)
    return analyzeMeter.analyzeMeter(poem)

if __name__ == '__main__':
    main('http://www.poetryfoundation.org/poems-and-poets/poems/detail/89189')
