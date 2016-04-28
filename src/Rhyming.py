'''
Created on Apr 9, 2016

@author: Donna
'''
from __future__ import absolute_import, print_function
import string
import re
import nltk


def find_end_in_dict(unknown_word):
    '''If a word is not in pronDict, find the
    pronunciation of its ending in pronDict'''
    pronDict = nltk.corpus.cmudict.dict()
    ending = ''
    unknown_word_list = [letter for letter in unknown_word]
    unknown_word_list.reverse()
    for letter in unknown_word_list:
        ending += letter
        if pronDict[ending] is not None:
            return pronDict[ending]


def rhyme_generator():
    '''Generate a list of letters to represent
    rhyme scheme'''
    letters = list(string.ascii_uppercase)
    index = 0
    while True:
        letter = letters[index % 26]
        new_letter = letter
        if index > 25:
            for i in range(index // 25):
                new_letter += letter
        yield new_letter
        index += 1


def find_rhyme_scheme(poem):
    '''Determine and return the poem's rhyme scheme'''
    vowels = [u'AO', u'AA', u'IY', u'UW', u'EH', u'IH', u'UH', u'AH', u'AX',
              u'AE', u'EY', u'AY', u'OW', u'AW', u'OY', u'ER', u'AXR',
              u'EH R', u'UH R', u'AO R', u'AA R', u'IH R', u'IY R', u'AW R']
    pronDict = nltk.corpus.cmudict.dict()
    # list of all the final syllables in the poem in order
    final_syllable_list = []
    # dict of syllables and their representative letters in the rhyme scheme
    rhyme_pairs = dict()
    # list of the rhyme scheme of the poem in ABBA format
    rhyme_scheme = []

    # Step 1: isolate the last syllable of the last word of every line
    for line in poem:
        line_lowercase = line.lower()
        # remove all dashes first
        line_no_dash = re.sub(r'[\'\,]', "", line_lowercase)
        # then remove all commas and other punctuation
        line_no_punc = re.sub(r'[^a-zA-Z\s]', " ", line_no_dash)
        word_list = line_no_punc.split()
        final_word = word_list[-1]
        if final_word in pronDict:
            # need to make a copy of pron so it doesn't reverse dict entry
            pron = []
            # if multiple pronunciations, pick the first one
            pron += pronDict[final_word][0]
            # extract final syllable: vowel plus optional consonant
            pron.reverse()
            for i, sound in enumerate(pron):
                # remove the numeric stress markers
                sound = re.sub(r'\d', "", sound)
                if sound in vowels:
                    if i is 0:
                        final_syllable_list.append(str(sound))
                    else:
                        # need the consonant sound as part of the rhyme
                        cons = pron[i-1]
                        final_syllable_list.append(str(sound) + str(cons))
                    break
        else:
            # search for a similar final syllable in pronDict
            pron = find_end_in_dict(final_word)[0]
            syllable = ""
            if pron is not None:
                for sound in pron:
                    # remove the numeric stress markers
                    sound = re.sub(r'\d', "", sound)
                    syllable += sound
                final_syllable_list.append(syllable)
            else:
                # if no pron in pronDict, signal that with '?'
                final_syllable_list.append('?')
                break

    # Step 2. Return rhyme scheme and number of distinct rhymes

    distinct_rhymes = []  # set of final syllables (no duplicates)
    for syllable in final_syllable_list:
        if syllable not in distinct_rhymes:
            distinct_rhymes.append(syllable)

    num_distinct_rhymes = len(distinct_rhymes)  # number of distinct rhymes

    # select letters to demonstrate rhyme scheme
    rhymes = rhyme_generator()

    # match up a rhyme with a letter
    for syllable, letter in zip(distinct_rhymes, rhymes):
        if syllable not in rhyme_pairs:
            rhyme_pairs[syllable] = letter

    for syllable in final_syllable_list:
        rhyme_scheme.append(rhyme_pairs[syllable])

    return rhyme_scheme
    print("This poem uses {} distinct rhymes.".format(num_distinct_rhymes))


if __name__ == '__main__':
    find_rhyme_scheme('Longfellow Hiawatha.txt')
