from cs50 import get_string
from decimal import *
import re


def main():
    sentence = get_string("Text: ").strip()
    length = len(sentence)
    # L = length / (sentence.count(" ") - 1) * 100
    letters = count_letters(sentence)
    # print("letters: " + str(letters))
    words = count_words(sentence)
    # print('words: ' + str(words))
    sentences = count_sentences(sentence)
    # print('sentences: ' + str(sentences))
    L = letters / words * 100
    S = sentences / words * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    # print(index)
    if (index < 1):
        print("Before Grade 1")
    elif (index > 15):
        print("Grade 16+")
    else:
        print("Grade " + str(round(index)))


def count_letters(sentence):
    p = re.compile('[a-z]', re.I)
    return len(p.findall(sentence))


def count_words(sentence):
    p = re.compile(r'\b[\w\'-]*[^\W]\b')
    wordslist = p.findall(sentence)
    # print(wordslist)
    words = len(wordslist)
    return words


def count_sentences(phrase):
    # p = re.compile(r'[\w\s,]*[^\W]', re.I)
    p = re.compile(r'[\w\s,\'\-\"\:\;]*[^\W]', re.I)
    sentencelist = p.findall(phrase)
    # print(sentencelist)
    sentences = len(sentencelist)
    return sentences


main()
