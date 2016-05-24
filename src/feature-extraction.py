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
import os

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
def pos_counter(postag):
    count = {}
    for k,v in postag:
        if v is not None:
            if v[0] in count:
                count[v[0]] = count[v[0]] + 1
            else:
                count[v[0]] = 1
    return count

#turns most common words in Latin into a list
def listifyWords():
    with open('words.txt') as f:
        toReturn = f.readlines()
    toReturn = [x.strip('\n') for x in toReturn]
    return toReturn

#counts instances of the ablative absolute, a Latin grammatical construction
#note that this likely undercounts ablative absolutes
def ablative_absolute(postag):
    count = 0
    temp = False
    for k,v in postag:
        if v is not None:
            #checks if the word is an adjective/participle/noun and is ablative
            if (v[0] is 'A' or v[0] is 'T' or v[0] is 'N') and v[7] is 'B':
                if temp is False:
                    temp = True
                else:
                    temp = False
                    count = count + 1
            else:
                temp = False
        else:
            temp = False
    return count

#avg words per sentence
def words_per_sentence(sentences):
    count = 0
    for s in sentences:
        count = count + len(s.split())
    return count / len(sentences)

#subjunctive use, passive voice use, infinitive use
def verb_use(postag):
    sub_count = 0
    pass_count = 0
    inf_count = 0
    verb_count = 0
    for k,v in postag:
        if v is not None and v[0] is 'V':
            verb_count = verb_count + 1
            if v[4] is "S":
                sub_count = sub_count + 1
            if v[5] is "P":
                pass_count = pass_count + 1
            if v[4] is "N":
                inf_count = inf_count + 1
    return [sub_count / verb_count, pass_count / verb_count, inf_count / verb_count]


# extract features from a single file
def feature_extract(filename, author):
    print(filename+" by "+author)
    jv = JVReplacer()
    words = WordTokenizer('latin')
    sentences = TokenizeSentence('latin')
    tagger = POSTag('latin')
    lem = LemmaReplacer('latin')

    f = open(filename+'.txt', 'r') #infile
    txt = f.read()

    f_out = open(filename+'.lat', 'w') #outfile

    print("wrangling text")
    jv.replace(txt) # regularizes use of "i/j" and "u/v" as these are interchangeable in Latin
    uppercase = txt
    txt = txt.lower() # make lower case

    txt = removeBrackets(txt)
    no_commas = removePunctuation(txt)

    print("finding parts of speech")
    word_tokens = words.tokenize(no_commas)
    sentence_tokens = sentences.tokenize_sentences(txt)
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
    print("parts of speech frequencies")
    pos_freq = pos_counter(parts_of_speech)
    verb_freq = verb_use(parts_of_speech)
    print("ablative absolute")
    abl = ablative_absolute(parts_of_speech)
    print("sentence analysis")
    wps = words_per_sentence(sentence_tokens)

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
            print(w + ": " + str(freq[w]/(len(word_tokens))))
            print(str(freq[w]/(len(word_tokens))), file=f_out)
        else:
            print(w + ": 0")
            print(0, file=f_out)
    named_entities = ne.count("Entity") / (len(word_tokens))
    print("ner: "+str(named_entities))
    print(str(named_entities), file=f_out)
    nt_count = txt.count("nt") / (len(no_commas))
    print("nt frequency: "+str(nt_count))
    print(str(nt_count), file=f_out)
    print("um:am ratio: "+str(um_am))
    print(str(um_am), file=f_out)
    for c in ['N','V','T','A','D','C','R','P']:
        if c in pos_freq:
            print(c + " POS: " + str(pos_freq[c]/(len(word_tokens))))
            print(str(pos_freq[c]/(len(word_tokens))), file=f_out)
        else:
            print(c + " POS: 0")
            print(0, file=f_out)
    print("ablative absolute: "+str(abl/len(word_tokens)))
    print(str(abl/len(word_tokens)), file=f_out)
    print("subjunctive frequency: "+str(verb_freq[0]))
    print(str(verb_freq[0]), file=f_out)
    print("passive frequency: "+str(verb_freq[1]))
    print(str(verb_freq[1]), file=f_out)
    print("infinitive frequency: "+str(verb_freq[2]))
    print(str(verb_freq[2]), file=f_out)
    print("words per sentence: "+str(wps))
    print(str(wps), file=f_out)
    author_count = txt.count(author.lower()) / (len(word_tokens))
    print("author name: "+str(author_count))
    print((author_count), file=f_out)

# main iterates through all files in a given directory
path = sys.argv[1]
if not path.endswith("/"):
    path = path + '/'

# create a dictionary of authors
with open('authors.txt') as authorfile:
    lines = authorfile.readlines()
lines = [x.strip('\n') for x in lines]
author_dict = {}
for line in lines:
    vals = line.split('\t')
    author_dict[vals[0]] = [vals[1], vals[2]]

outfile = input("Dataset Filename: ")
outf = open(outfile, "w")

for filename in os.listdir(sys.argv[1]):
    if filename.endswith(".txt"):
        # first, run feature extraction
        filename = filename[:-4] #remove last 4 characters, aka .txt
        author = author_dict[filename][0]
        feature_extract(path+filename, author)

        # then add to a larger dataset file
        inf = open(path+filename+".lat", "r")
        count = 1
        classification = author_dict[filename][1]
        outline = str(classification)+" "
        for line in inf.readlines():
            line = line[:-1]
            outline = outline + str(count) + ":" + line + " "
            count = count + 1
        print(outline, file=outf)
        inf.close()
