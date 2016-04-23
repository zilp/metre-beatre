'''
Created on Apr 17, 2016

@author: Donna
'''
from __future__ import absolute_import, print_function
import string
import re
import nltk

def assonance(text):
    vowels = ['AO','AA','IY','UW','EH','IH','UH','AH','AX','AE','EY','AY','OW',\
              'AW','OY','ER','AXR','EH R','UH R','AO R','AA R','IH R','IY R',\
              'AW R']
    extras = ['a', 'an', 'the', 'that', 'those', 'these', 'and']
    pronDict = nltk.corpus.cmudict.dict()
    assonance_by_line = []
    try:
        poem = open(text, 'r')
        raw_lines = poem.readlines()
        for line in raw_lines:
            soundDict = dict()
            assonance = []
            line_lowercase = line.lower()
            line_no_punc = re.sub(r'[^a-zA-Z\s]', ' ', line_lowercase)  # remove all commas and other punctuation
            word_list = line_no_punc.split()
            for word in word_list:
                if word not in pronDict:
                    continue
                else:
                    pron = pronDict[word][0]
                    for sound in pron:
                        sound = re.sub(r'[\d]', "", sound)
                        if sound in vowels:
                            if sound not in soundDict:
                                soundDict[sound] = [word]
                            else:
                                word_list = soundDict[sound]
                                soundDict[sound] = word_list + [word]
                    for list in soundDict.values():
                        if len(list) >= 2:
                            assonance.append(word)
                assonance = [w for w in assonance if w not in extras]
                if len(assonance) > 1:
                    assonance_by_line.append(assonance)
        print(assonance_by_line)     
    except IOError:
        return "File not found."
    finally:
        poem.close()

if __name__ == '__main__':
    assonance('Thomas Do Not Go Gentle.txt')