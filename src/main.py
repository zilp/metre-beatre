'''
Created on Apr 24, 2016

@author: shilpa
'''
from parser import get_text
import parser, parser_alt, analyzeMeter, Rhyming

# used by server
def main(url):
    poem = []
    if "poets.org" in url:
        poem = parser_alt.get_text_alt(url)
    elif "poetryfoundation" in url:
        poem = parser.get_text(url)
    else:
        return "Invalid input."
    print analyzeMeter.analyzeMeter(poem) + '\n' + Rhyming.rhyme(poem)
    return analyzeMeter.analyzeMeter(poem) + '\n' + Rhyming.rhyme(poem)

if __name__ == '__main__':
    main('http://www.poetryfoundation.org/poems-and-poets/poems/detail/89189')
