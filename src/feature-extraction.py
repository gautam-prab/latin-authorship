from cltk.tokenize.word import WordTokenizer
from cltk.tag.pos import POSTag
from cltk.tokenize.sentence  import TokenizeSentence
from cltk.tag import ner # named entity recognition
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
import math
import statistics
import collections
import sys

# iterates thru text and removes every thing in []
# this is useful for prose with line numbers that we don't want to analyze
def removeBrackets(txt):
    newstring = ""
    flag = False
    for c in txt:
        if c == '[':
            flag = True
        elif c == ']':
            flag = False
        else:
            if not flag:
                newstring = newstring + c
    return newstring

#removes unneeded punctuation from text
def removePunctuation(txt):
    newstring = ""
    flag = False
    for c in txt:
        if not (c == '.' or c == ',' or c == ';' or c == ':' or c == '!' or c == '?'):
            newstring = newstring + c
    return newstring

#finds the hapax legomena and dis legomena values
#this is the number of words that appear exactly once and exactly twice
def legomena(lemmas): #iterable is the list of lemmas
    tuples = [tuple(x) for x in lemmas]
    counts = collections.Counter(tuples)
    hapax = []
    dis = []
    for t in tuples:
        if counts[t] == 1: #exactly once
            hapax.append(t)
        elif counts[t] == 2 and t not in dis: #exactly twice
            dis.append(t)
    return hapax, dis

#finds frequency of each lemma in the text
def word_frequencies(lemmas):
    frequency_dictionary = {}
    for l in lemmas:
        if l in frequency_dictionary:
            frequency_dictionary[l] = frequency_dictionary[l] + 1
        else:
            frequency_dictionary[l] = 1
    return frequency_dictionary

#finds the ratio of "um" to "am" as word endings
def um_am_ratio(words):
    um = 0
    am = 0
    for word in words:
        if word.endswith("um"):
            um = um + 1
        elif word.endswith("am"):
            am = am + 1
    return um/am

#counts conjunctions
def conjunction_counter(postag):
    count = 0
    for k,v in postag:
        if v is not None and v[0] is 'C':
            count = count + 1
    return count

#turns most common words in Latin into a list
def listifyWords():
    with open('words.txt') as f:
        toReturn = f.readlines()
    toReturn = [x.strip('\n') for x in toReturn]
    return toReturn

# main

if (len(sys.argv) < 3):
    print("input required")

jv = JVReplacer()
words = WordTokenizer('latin')
tagger = POSTag('latin')
lem = LemmaReplacer('latin')

f = open(sys.argv[1]+'.txt', 'r') #infile
txt = f.read()

f_out = open(sys.argv[1]+'.lat', 'w') #outfile

print("wrangling text")
jv.replace(txt) # regularizes use of "i/j" and "u/v" as these are interchangeable in Latin
uppercase = txt
txt = txt.lower() # make lower case

txt = removeBrackets(txt)
no_commas = removePunctuation(txt)

print("finding parts of speech")
word_tokens = words.tokenize(no_commas)
lemma_tokens = lem.lemmatize(no_commas)
parts_of_speech = tagger.tag_ngram_123_backoff(no_commas)

print("word lengths")
word_lengths = []
for word in word_tokens:
    word_lengths+=[len(word)]

avg_word_length = (statistics.mean(word_lengths) - 6.3)
st_dev = statistics.stdev(word_lengths)

print("legomena")
hapax, dis = legomena(lemma_tokens)
freq = word_frequencies(lemma_tokens)
print("named entities")
ne = ner.tag_ner('latin', input_text=uppercase, output_type=str)
print("um/am")
um_am = um_am_ratio(word_tokens)
print("conjunctions")
conj = conjunction_counter(parts_of_speech) / (len(word_tokens)/10)

print("number of words: " + str(len(word_tokens)))
print("average word length: " + str(avg_word_length))
print(str(avg_word_length), file=f_out)
print("standard deviation word length: " + str(st_dev))
print(str(st_dev), file=f_out)
print("hapax legomena: " + str(len(hapax) / len(freq)))
print(str(len(hapax) / len(freq)), file=f_out)
print("dis legomena: " + str(len(dis) / len(freq)))
print(str(len(dis) / len(freq)), file=f_out)
print("richness: " + str(len(freq) / len(word_tokens)))
print(str(len(freq) / len(word_tokens)), file=f_out)
commonWords = listifyWords()
for w in commonWords: #prints the most common Latin words as frequencies
    w = lem.lemmatize(w, return_string = True)
    if w in freq.keys():
        print(w + ": " + str(freq[w]/(len(word_tokens)/10)))
        print(str(freq[w]/(len(word_tokens)/10)), file=f_out)
    else:
        print(w + ": 0")
        print(0, file=f_out)
named_entities = ne.count("Entity") / (len(word_tokens) / 10)
print("ner: "+str(named_entities))
print(str(named_entities), file=f_out)
nt_count = txt.count("nt") / (len(no_commas) / 10)
print("nt frequency: "+str(nt_count))
print(str(nt_count), file=f_out)
print("um:am ratio: "+str(um_am))
print(str(um_am), file=f_out)
print("conjunction count: "+str(conj))
print(str(conj), file=f_out)
author_count = txt.count(sys.argv[2].lower()) / (len(word_tokens)/10)
print("author name: "+str(author_count))
print((author_count), file=f_out)
