'''
Created on Apr 14, 2016

@author: Donna
'''

from __future__ import absolute_import, print_function
import string
import re
import nltk

def alliteration(text):
    vowels = [u'AO',u'AA',u'IY',u'UW',u'EH',u'IH',u'UH',u'AH',u'AX',u'AE',\
              u'EY',u'AY',u'OW',u'AW',u'OY',u'ER',u'AXR',u'EH R',u'UH R',\
              u'AO R',u'AA R',u'IH R',u'IY R',u'AW R']
    extras = ['a', 'an', 'the', 'that', 'those', 'these', 'and']
    pronDict = nltk.corpus.cmudict.dict()
    alliteration_by_line = []
    try:
        poem = open(text, 'r')
        raw_lines = poem.readlines()
        for line in raw_lines:
            soundDict = dict()
            alliteration = []
            line_lowercase = line.lower()
            line_no_punc = re.sub(r'[^a-zA-Z\s]', ' ', line_lowercase)  # remove all commas and other punctuation
            word_list = line_no_punc.split()
            for word in word_list:
                try:
                    pron = pronDict[word]
                except KeyError:
                    continue
#                     porter = nltk.PorterStemmer()
#                     stem = porter.stem(word)
#                     pron = pronDict[stem]
                first_sound = pron[0][0]
                if first_sound in vowels:
                    if len(soundDict[vowels]) is 0:
                        soundDict[vowels] = [word]
                    else:
                        vowel_word_list = soundDict[vowels]
                        soundDict[vowels] = vowel_word_list + [word]
                elif first_sound not in soundDict.keys():
                    soundDict[first_sound] = [word]
                else:
                    allit_word_list = soundDict[first_sound]
                    soundDict[first_sound] = allit_word_list + [word]
            for sound in soundDict.keys():
                if len(soundDict[sound]) >= 2:
                    for word in soundDict[sound]:
                        alliteration.append(word)
            alliteration = [w for w in alliteration if w not in extras]
            if len(alliteration) > 1:
                alliteration_by_line.append(alliteration)
        print(alliteration_by_line)
        #print([w for w in alliteration_by_line if w not in extras])
    except IOError:
        return "File not found"
    finally:
        poem.close()

if __name__ == '__main__':
    alliteration('Millay Sonnet 42.txt')