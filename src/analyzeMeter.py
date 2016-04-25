'''
Created on Apr 5, 2016

@author: zhi
'''
from __future__ import absolute_import, division, print_function
import nltk
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.metrics.distance import edit_distance


def num_syllables(word):
    diphthongs = ['ou', 'ie', 'igh', 'oi', 'oy', 'oo', 'ea', 'ee', 'ai', 
              'ure', 'ough']
    vowels = ['a', 'e', 'i', 'o', 'u']
    exceptions = ['quo', 'qua', 'qui', 'que']
    syllables = 0
    for d in diphthongs:
        if d in word:
            syllables += 1
            word = re.sub(d, "", word)
    for letter in word:
        if letter in vowels:
            syllables += 1
    #take out count for final, silent 'e'
    if word[-1] is 'e':
        syllables -= 1
    #take out count for suffix 'ed'
    if re.search(r'ed$|qu(a|e|i|o)', word) is not None:
        syllables -= 1
    return syllables


def split_syllables(word):
    regex = re.compile(r'(ou)|(ie)|(igh)|(oi)|(oy)|(oo)|(ea)|(ee)|(ai)|(ure)|\
        (ough)|(a)|(e)|(i)|(o)|(u)|(quo)')
    raw_split = re.split(regex, word) # has None as several elements
    return [x for x in raw_split if x is not None and x is not '']


def find_meter(word):
    diphthongs = ['ou', 'ie', 'igh', 'oi', 'oy', 'oo', 'ea', 'ee', 'ai', 
              'ure', 'ough']
    vowels = ['a', 'e', 'i', 'o', 'u']
    exceptions = ['quo', 'qua', 'qui', 'que']
    result = ""
    if word[-1] is 'e':
        word = word[:-1]
    elif word[-2] is 'e' and word[-1] is 'd':
        word = word[:-2]
    sylls = split_syllables(word)
    for e in sylls:
        if e in vowels:
            result += "0"
        elif e in diphthongs or e in exceptions:
            result += "1"
    return result

def find_closest_word_with_regex(regex, list=nltk.corpus.cmudict.dict().keys()):
    for e in list:
        result = re.search(regex, e)
        if result is not None:
            return e
        else:
            continue 
        

def remove_affixes(word):
    stemmer = SnowballStemmer("english")
    regex = re.compile(r'(^un)|(^non)')
    stem = re.sub(regex, "", stemmer.stem(word))
    return stem


def find_closest_word(word):
    stem = remove_affixes(word)
    regex = re.compile(stem)
    return find_closest_word_with_regex(regex)


def finish_meter(unknown_word, pronDict = nltk.corpus.cmudict.dict()):
    
    found_word = find_closest_word(unknown_word)
    unknown_word_syllables = num_syllables(unknown_word)
    
    if found_word is None:
        return find_meter(unknown_word)
    else:
        found_word_pron = pronDict[found_word]
        found_word_pron_list = "".join(found_word_pron[0])
        found_word_raw_stress = "".join(re.findall(r'\d+', found_word_pron_list))
        found_word_stress = re.sub("2", "1", found_word_raw_stress)
        return found_word_stress


def simpleCleanup(s):
    s = re.sub("\(1\|1\)", "1", s)
    s = re.sub("\(0\|0\)", "0", s)
    s = re.sub("\(10\|10\)", "10", s)
    s = re.sub("\(01\|01\)", "01", s)
    return s


def iambEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "0":
            place = 1
            result += value
        elif place == 1 and l == "1":
            place = 0
            result += value
    return result


def trocheeEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "1":
            place = 1
            result += value
        elif place == 1 and l == "0":
            place = 0
            result += value
    return result


def anapestEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "0":
            place = 1
            result += value
        elif place == 1 and l == "0":
            place = 2
            result += value
        elif place == 2 and l == "1":
            place = 0
            result += value
    return result


def dactylEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "1":
            place = 1
            result += value
        elif place == 1 and l == "0":
            place = 2
            result += value
        elif place == 2 and l == "0":
            place = 0
            result += value
    return result


def amphibrachEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "0":
            place = 1
            result += value
        elif place == 1 and l == "1":
            place = 2
            result += value
        elif place == 2 and l == "0":
            place = 0
            result += value
    return result


def analyzeMeter(poem):
    pronDict = nltk.corpus.cmudict.dict()
    type = {"iamb": 0, "trochee": 0,
            "anapest": 0, "dactyl": 0, "amphibrach": 0}
    meterlength = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sumvalue = 0
    reg = re.compile('[^a-zA-Z\']')
    for s in poem:
        meterstress = ""
        currentMeter = 0
        twoSyCount = 0
        threeSyCount = 0
        line_lowercase = s.lower()
        line_no_dash = re.sub(r'[\'\,]', "", line_lowercase)
        line_no_punc = re.sub(r'[^a-zA-Z\s]', " ", line_no_dash)  # remove all commas and other punctuation
        word_list = line_no_punc.split()
        for w in word_list:
            if w in pronDict:
                pronparse = pronDict[w]
                if len(pronparse) == 1:
                    teststr = "".join(pronparse[0])
                    temp = "".join(re.findall(r'\d+', teststr))
                    temp = re.sub("2", "1", temp)
                    meterstress += temp
                    if len(temp) == 1:
                        type["iamb"] += 2
                        type["trochee"] += 2
                        type["anapest"] += 2
                        type["dactyl"] += 2
                        type["amphibrach"] += 2
                    else:
                        type["iamb"] += iambEstimate(temp, twoSyCount, 4)
                        type["trochee"] += trocheeEstimate(temp, twoSyCount, 4)
                        type["anapest"] += anapestEstimate(temp, threeSyCount, 4)
                        type["dactyl"] += dactylEstimate(temp, threeSyCount, 4)
                        type["amphibrach"] += amphibrachEstimate(temp, threeSyCount, 4)
                    twoSyCount = (twoSyCount + len(temp)) % 2
                    threeSyCount = (threeSyCount + len(temp)) % 3
                    sumvalue += 4 * len(temp)
                    currentMeter += len(temp)
                else:
                    # need to figure out what to do for multi pronouncations
                    meterstress += '('
                    count = 1
                    for word in pronparse:
                        teststr = "".join(word)
                        temp = "".join(re.findall(r'\d+', teststr))
                        temp = re.sub("2", "1", temp)
                        type["iamb"] += iambEstimate(temp, twoSyCount, 1)
                        type["trochee"] += trocheeEstimate(temp, twoSyCount, 1)
                        type["anapest"] += anapestEstimate(temp, threeSyCount, 1)
                        type["dactyl"] += dactylEstimate(temp, threeSyCount, 1)
                        type["amphibrach"] += amphibrachEstimate(temp, threeSyCount, 1)
                        if count < len(pronparse):
                            count += 1
                            meterstress += temp + '|'
                        else:
                            count = 1
                            meterstress += temp + ')'
                    teststr = "".join(pronparse[0])
                    temp = "".join(re.findall(r'\d+', teststr))
                    twoSyCount = (twoSyCount + len(temp)) % 2
                    threeSyCount = (threeSyCount + len(temp)) % 3
                    sumvalue += 1 * len(temp)
                    currentMeter += len(temp)
            else:
                # need to figure out if word is not in cmudict
                print("Can't find", w)
                found_meter = finish_meter(w)
                print(found_meter)
                meterstress += found_meter
                type["iamb"] += iambEstimate(found_meter, twoSyCount, 1)
                type["trochee"] += trocheeEstimate(found_meter, twoSyCount, 1)
                type["anapest"] += anapestEstimate(found_meter, threeSyCount, 1)
                type["dactyl"] += dactylEstimate(found_meter, threeSyCount, 1)
                type["amphibrach"] += amphibrachEstimate(found_meter, threeSyCount, 1)
                twoSyCount = (twoSyCount + len(found_meter)) % 2
                threeSyCount = (threeSyCount + len(found_meter)) % 3
                sumvalue += 1 * len(found_meter)
        meterstress = simpleCleanup(meterstress)
        print(meterstress)
        if currentMeter < 17:
            meterlength[currentMeter] += 1

    best_fit = ""
    temp_max = 0
    beat = 2
    if(type["iamb"] > temp_max):
        temp_max = type["iamb"]
        best_fit = "iambic"
    if(type["trochee"] > temp_max):
        temp_max = type["trochee"]
        best_fit = "trochaic"
    if(type["anapest"] > temp_max):
        temp_max = type["anapest"]
        best_fit = "anapestic"
        beat = 3
    if(type["dactyl"] > temp_max):
        temp_max = type["dactyl"]
        best_fit = "dactylic"
        beat = 3
    if(type["amphibrach"] > temp_max):
        temp_max = type["amphibrach"]
        best_fit = "amphibrachic"
        beat = 3

    lengthtype = ["monometer", "dimeter", "trimeter", "tetrameter", 
                  "pentameter", "hexameter", "heptameter", "octameter"]
    print("Likelyhood to be iamb is", type["iamb"] / sumvalue)
    print("Likelyhood to be trochee is", type["trochee"] / sumvalue)
    print("Likelyhood to be anapest is", type["anapest"] / sumvalue)
    print("Likelyhood to be dactyl is", type["dactyl"] / sumvalue)
    print("Likelyhood to be amphibrach is", type["amphibrach"] / sumvalue)

    print("Best meter fit is", best_fit, lengthtype[(meterlength.index(max(meterlength))-1)//beat])
    return best_fit


def printPoemStress(poem, meter):
    result = []
    index = 0
    if meter == "iambic":
        printMap = ["U", "/"]
        beat = 2
    elif meter == "trochaic":
        printMap = ["/", "U"]
        beat = 2
    elif meter == "dactylic":
        printMap = ["/", "U", "U"]
        beat = 3
    elif meter == "anapestic":
        printMap = ["U", "U", "/"]
        beat = 4
    elif meter == "amphibrachic":
        printMap = ["U", "/", "U"]
        beat = 5
    for line in poem:
        line = line.lower()
        count = 0
        new = True
        following = False
        result.append(line)
        for i in range(len(line)):
            w = line[i]
            if w == "a" or w == "i" or w == "o" or w == "u" or w == "y":
                if not following:
                    result.append(printMap[count % beat])
                    following = True
                    new = False
                    count += 1
                else:
                    result.append(" ")
            elif w == "e":
                if new:
                    result.append(printMap[count % beat])
                    following = True
                    new = False
                    count += 1
                elif not line[i+1].isalpha():
                    result.append(" ")
                elif (line[i+1] == "d" or line[i+1] == "s") and not line[i+2].isalpha() and line[i-1] != "l":
                    result.append(" ")
                else:
                    result.append(printMap[count % beat])
                    following = True
                    new = False
                    count += 1
            elif w == " ":
                new = True
                following = False
                result.append(" ")
            else:
                result.append(" ")
                following = False
        result.append("\n")

    return "".join(result)


poem = open('Shelley Witch of Atlas.txt', 'r')
raw_lines = poem.readlines()
meter = analyzeMeter(raw_lines)
result = printPoemStress(raw_lines, meter)
print(result)