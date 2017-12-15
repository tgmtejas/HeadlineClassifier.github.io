import numpy as np
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys, unicodedata
import random     

table = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))

english_stopwords = stopwords.words('english')
english_stopwords = [str(x) for x in english_stopwords]

stemmer = PorterStemmer()

stats_words_b = {}
stats_words_t = {}
stats_words_e = {}
stats_words_m = {}

total_b = 0
total_t = 0
total_e = 0
total_m = 0

f = open('newsCorpora.csv')
data = f.readlines()

random.shuffle(data)
random.shuffle(data)
random.shuffle(data)
random.shuffle(data)

w = data[:(len(data)/8)]
f.close()

for i in w:
    temp_list = i.decode('utf-8').strip().split('\t')
    headline = temp_list[1]
    cat = temp_list[4]
    words = headline.split()
    words_cleaned = [x.translate(table).lower() for x in words]
    words_cleaned_stopwords = [stemmer.stem(x) for x in words_cleaned if x not in english_stopwords]    
    while '' in words_cleaned_stopwords:
        words_cleaned_stopwords.remove('')

    if cat=='b':
        total_b += 1
        for j in words_cleaned_stopwords:
            if j in stats_words_b:
                stats_words_b[j] += 1
            else:
                stats_words_b[j] = 1
    if cat=='t':
        total_t += 1
        for j in words_cleaned_stopwords:
            if j in stats_words_t:
                stats_words_t[j] += 1
            else:
                stats_words_t[j] = 1
    if cat=='e':
        total_e += 1
        for j in words_cleaned_stopwords:
            if j in stats_words_e:
                stats_words_e[j] += 1
            else:
                stats_words_e[j] = 1
    if cat=='m':
        total_m += 1
        for j in words_cleaned_stopwords:
            if j in stats_words_m:
                stats_words_m[j] += 1
            else:
                stats_words_m[j] = 1


b_word_asc = sorted(stats_words_b, key=lambda k: stats_words_b[k])
b_word_asc.reverse()
t_word_asc = sorted(stats_words_t, key=lambda k: stats_words_t[k])
t_word_asc.reverse()
e_word_asc = sorted(stats_words_e, key=lambda k: stats_words_e[k])
e_word_asc.reverse()
m_word_asc = sorted(stats_words_m, key=lambda k: stats_words_m[k])
m_word_asc.reverse()

vocabulary = b_word_asc[:2000] + e_word_asc[:2000] + t_word_asc[:2000] + m_word_asc[:2000] 

count = 0

p_vocabulary_given_b = {}
p_vocabulary_given_t = {}
p_vocabulary_given_m = {}
p_vocabulary_given_e = {}


for i in vocabulary:

    if i in stats_words_b:
        p_vocabulary_given_b[i] = float(stats_words_b[i] + 1)/(float(total_b) + float(len(vocabulary)))
    else:
        p_vocabulary_given_b[i] = (1.0)/(float(total_b) + float(len(vocabulary)))

    if i in stats_words_t:
        p_vocabulary_given_t[i] = float(stats_words_t[i] + 1)/(float(total_t) + float(len(vocabulary)))
    else:
        p_vocabulary_given_t[i] = (1.0)/(float(total_t) + float(len(vocabulary)))

    if i in stats_words_e:
        p_vocabulary_given_e[i] = float(stats_words_e[i] + 1)/(float(total_e) + float(len(vocabulary)))
    else:
        p_vocabulary_given_e[i] = (1.0)/(float(total_e) + float(len(vocabulary)))

    if i in stats_words_m:
        p_vocabulary_given_m[i] = float(stats_words_m[i] + 1)/(float(total_m) + float(len(vocabulary)))
    else:
        p_vocabulary_given_m[i] = (1.0)/(float(total_m) + float(len(vocabulary)))


	
    

