'''
Created on Apr 24, 2016

@author: shilpa
'''
from parser_orig import get_text
import parser_orig
import parser_alt
import analyzeMeter
import Rhyming


# used by server
def main(url):
    poem = []
    if "poets.org" in url:
        title = parser_alt.get_text_alt(url)[0]
        poem = parser_alt.get_text_alt(url)[1]
    elif "poetryfoundation" in url:
        title = parser_orig.get_text(url)[0]
        poem = parser_orig.get_text(url)[1]
    else:
        return "Invalid input."
    print poem
    result = analyzeMeter.analyzeMeter(poem)
    scansion = analyzeMeter.printPoemStress(poem, result[0])
    rhyme = str(Rhyming.find_rhyme_scheme(poem))
    return '\n' + title + '\n\n' + "METER" + '\n' + result[0] + " " +
    result[1] + '\n\n' + "RHYME SCHEME" + '\n' + rhyme + '\n\n' +
    "SCANSION" + '\n' + scansion


if __name__ == '__main__':
    main('http://www.poetryfoundation.org/poems-and-poets/poems/detail/43644"')
