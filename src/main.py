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
    result = analyzeMeter.analyzeMeter(poem)
    scansion = analyzeMeter.printPoemStress(poem, result[0])
    rhyme = str(Rhyming.rhyme(poem))
    print result[0] + " " + result[1] + '\n' + rhyme + '\n' + scansion
    return str((result[0], result[1], rhyme, scansion))


if __name__ == '__main__':
    main('http://www.poetryfoundation.org/poems-and-poets/poems/detail/89189')
