'''
Created on Apr 24, 2016

@author: shilpa
'''

import parser_foundation
import parser_poets
import analyzeMeter
import Rhyming


# used by server
def main(url):
    poem = []
    if "poets.org" in url:
        title = parser_poets.get_text(url)[0]
        poem = parser_poets.get_text(url)[1]
    elif "poetryfoundation" in url:
        title = parser_foundation.get_text(url)[0]
        poem = parser_foundation.get_text(url)[1]
    else:
        return "Invalid input."
    result = analyzeMeter.analyzeMeter(poem)
    scansion = analyzeMeter.printPoemStress(poem, result[0])
    rhyme = str(Rhyming.find_rhyme_scheme(poem))
    return '\n' + title + '\n\n' + "METER" + '\n' + result[0] + " " +\
        result[1] + '\n\n' + "RHYME SCHEME" + '\n' + rhyme + '\n\n' +\
        "SCANSION" + '\n' + SCANSION


if __name__ == '__main__':
    main('http://www.poetryfoundation.org/poems-and-poets/poems/detail/43644"')
