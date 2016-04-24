'''
Created on Apr 5, 2016

@author: zhi
'''
from __future__ import absolute_import, division, print_function
import nltk
import re


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


def spondeeEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "1":
            place = 1
            result += value
        elif place == 1 and l == "1":
            place = 0
            result += value
    return result


def pyrrhicEstimate(syllable, place, value):
    result = 0
    for l in syllable:
        if place == 0 and l == "0":
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
    type = {"iamb": 0, "trochee": 0, "spondee": 0, "pyrrhic": 0,
            "anapest": 0, "dactyl": 0, "amphibrach": 0}
    meterlength = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sumvalue = 0
    reg = re.compile('[^a-zA-Z\']')
    for s in poem:
        meterstress = ""
        currentMeter = 0
        twoSyCount = 0
        threeSyCount = 0
        for w in s.split():
            w = re.sub(reg, "", w)
            w = w.lower()
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
                print("Cant find", w)

        meterstress = simpleCleanup(meterstress)
        print(meterstress)
        if currentMeter < 16:
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


if __name__ == "__main__":
    poem = open('monarch.txt', 'r')
    raw_lines = poem.readlines()
    analyzeMeter(raw_lines)
