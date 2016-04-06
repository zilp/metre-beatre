'''
Created on Apr 5, 2016

@author: zhi
'''
from __future__ import absolute_import, division, print_function
from nltk.corpus import cmudict
import re


def main():
    pronDict = cmudict.dict()
    reg = re.compile('[^a-zA-Z\']')
    s = raw_input("Enter a string to analyze: ")
    meterstress = ""
    for w in s.split():
        w = re.sub(reg, "", w)
        if w in pronDict:
            pronparse = pronDict[w]
            if len(pronparse) == 1:
                teststr = "".join(pronparse[0])
                meterstress += "".join(re.findall(r'\d+', teststr))
            else:
                #need to figure out what to do for multi pronouncations
                teststr = "".join(pronparse[0])
                meterstress += "".join(re.findall(r'\d+', teststr))
        else:
            #need to figure out if word is not in cmudict
            print("Cant find", w)
    print(meterstress)


if __name__ == "__main__":
    main()
