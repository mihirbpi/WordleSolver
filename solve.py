import itertools
import math
import re
import numpy as np
from collections import defaultdict

all_words = [x.strip() for x in open("possible-words.txt").readlines()]

patterns = list(itertools.product('byg', repeat=5))

def pattern_and_word_to_reg(word, pattern):

        reg_list = []
        for i in range(0, 5):
            reg_list.append("_")

        bs = ""
        ys = []
        gs = []
        special = set()
        counts = None
        counts = defaultdict(lambda:0)

        for i in range(0, 5):

            if(pattern[i] == "g"):
                reg_list[i] = word[i]
                gs.append(word[i])
                counts[word[i]] += 1

            elif(pattern[i] == "y"):
                ys.append(word[i])
                counts[word[i]] += 1
                special.add(word[i])

        for i in range(0, 5):

            if(pattern[i] == "b" and (word[i] not in gs) and (word[i] not in ys)):
                bs += word[i]

            elif(pattern[i] == "b"):
                special.add(word[i])

        for i in range(0, 5):

            if(reg_list[i] == "_"):

                if(len(bs) > 0):
                    reg_list[i] = "[^"+bs+"]"
                else:
                    reg_list[i] = "."

        for i in range(0, 5):

            if(pattern[i] == "y"):
                reg_list[i] = "[^"+reg_list[i][1:-1] + word[i] + "]"

        return ("".join(reg_list), list(special), counts)


def get_matching_words(word, pattern, all_words_list):
    reg_result = pattern_and_word_to_reg(word, pattern)
    #print(reg_result)
    reg = r'{0}'.format(reg_result[0])
    matches = []

    for w in all_words_list:

        b = True

        for l in reg_result[1]:

            if(w.count(l) < reg_result[2][l]):
                b = False

        if ((re.fullmatch(reg, w) != None) and b):
            matches.append(w)

    return matches

'''
def get_pattern(real_word, guess):
    for pattern in patterns:
        reg = r'{0}'.format(pattern_and_word_to_reg(guess, pattern)[0])
        if(re.fullmatch(reg, real_word) != None and guess != real_word):
            return pattern
'''

def entropy(word, all_words_list):
    s = 0

    for pattern in patterns:
        matches = get_matching_words(word, pattern, all_words_list)
        p = float(len(matches) / len(all_words_list))

        if (p != 0):
            s += p * np.log(1/p) / np.log(2.0)
    return s


def get_best_word(current_word, all_words_list):

    if(len(all_words_list) == 1):
        return all_words_list[0]

    best_entropy = 0
    best_index = 0

    for i in range(0, len(all_words_list)):
        w = all_words[i]
        e = entropy(w, all_words_list)

        if(e >= best_entropy):
            best_entropy = e
            best_index = i

    return all_words_list[best_index]


guess = "tares"
solved = False
num_guesses = 1

while (not solved):
    print("The next guess should be: " + guess)
    pattern = input("Enter the pattern displayed after this guess: ")

    if(pattern=="ggggg"):
        break

    all_words = get_matching_words(guess, pattern, all_words)
    print("There are now "+str(len(all_words))+" words that match all the currently shown patterns")
    print(all_words)

    if(len(all_words) == 1):
        num_guesses += 1
        print("Calculating next guess...")
        guess = get_best_word(guess, all_words)

    else:
        print("Calculating next guess...")
        guess = get_best_word(guess, all_words)
        num_guesses += 1

print("Solved the puzzle in "+str(num_guesses)+ " guesses")
