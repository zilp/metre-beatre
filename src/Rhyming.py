'''
Created on Apr 9, 2016

@author: Donna
'''
from __future__ import absolute_import, print_function
import string
import re
import nltk


def rhyme(poem):
    vowels = [u'AO',u'AA',u'IY',u'UW',u'EH',u'IH',u'UH',u'AH',u'AX',u'AE',\
              u'EY',u'AY',u'OW',u'AW',u'OY',u'ER',u'AXR',u'EH R',u'UH R',\
              u'AO R',u'AA R',u'IH R',u'IY R',u'AW R']
    pronDict = nltk.corpus.cmudict.dict()
    final_syllable_list = [] # list of all the final syllables in the poem in order
    rhyme_pairs = dict() # dict of the syllables and their representative letters in the rhyme scheme
    rhyme_scheme = [] # list of the rhymes in the poem in ABBA format


    try:
        for line in poem:
            line_lowercase = line.lower()
            line_no_punc = re.sub(r'[^a-zA-Z\s]', '', line_lowercase)  # remove all commas and other punctuation
            word_list = line_no_punc.split()
            final_word = word_list[-1]
            if final_word in pronDict:
                pron = pronDict[final_word][0] # if multiple pronunciations, pick the second one

                # extract final syllable: vowel plus optional consonant
                pron.reverse()
                for i, sound in enumerate(pron):
                    sound = re.sub(r'\d', "", sound) # remove the nuumeric stress markers
                    if sound in vowels:
                        if i is 0:
                            final_syllable_list.append(str(sound))
                        else:
                            cons = pron[i-1]
                            final_syllable_list.append(str(sound) + str(cons))
                        break

            else:
                return "Following word not in dictionary: {}".format(final_word)

    except IOError:
        return "File not found."
    finally:
        poem.close()

    print("Final syllable list is {}".format(final_syllable_list))

    final_syllables = []
    for syllable in final_syllable_list:
        if syllable not in final_syllables:
            final_syllables.append(syllable)

    print("Final syllables are {}".format(final_syllables))
    num_syllables = len(final_syllables)

    rhymes = string.ascii_uppercase[:num_syllables]

    for syllable, letter in zip(final_syllables, rhymes):
        if syllable not in rhyme_pairs:
            rhyme_pairs[syllable] = letter

    for syllable in final_syllable_list:
        print(syllable)
        rhyme_scheme.append(rhyme_pairs[syllable])

    return rhyme_scheme


if __name__ == '__main__':
    main()
