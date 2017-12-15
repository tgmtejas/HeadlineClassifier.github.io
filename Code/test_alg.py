import numpy as np
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys, unicodedata
import train_stats
        

def classify(cleaned_headline,p_vocabulary_given_m,p_vocabulary_given_t,p_vocabulary_given_e,p_vocabulary_given_b,total_b,
             total_t, total_m,total_e):
    log_p_b = 0
    log_p_e = 0
    log_p_m = 0
    log_p_t = 0
    vocabulary_l = float(len(p_vocabulary_given_m))
    total_data = float(total_b + total_e + total_t + total_m) 
    
    for i in cleaned_headline:
        if i in p_vocabulary_given_b:
            log_p_b += np.log(p_vocabulary_given_b[i])
        else:
            log_p_b += (np.log(1.0/(float(total_b)+ 52867)))
            
        if i in p_vocabulary_given_t:
            log_p_t += np.log(p_vocabulary_given_t[i])
        else:
            log_p_t += (np.log(1.0/(float(total_t)+ 52867)))
            
        if i in p_vocabulary_given_e:
            log_p_e += np.log(p_vocabulary_given_e[i])
        else:
            log_p_e += (np.log(1.0/(float(total_e)+ 52867)))
            
        if i in p_vocabulary_given_m:
            log_p_m += np.log(p_vocabulary_given_m[i])
        else:
            log_p_m += (np.log(1.0/(float(total_m)+52867)))
            
    log_p_b += np.log(total_b/total_data)
    log_p_t += np.log(total_t/total_data)
    log_p_e += np.log(total_e/total_data)
    log_p_m += np.log(total_m/total_data)

    max_log_p = max(log_p_b,log_p_e,log_p_t,log_p_m)

    if log_p_b == max_log_p:
        return 'b'
    if log_p_t == max_log_p:
        return 't'
    if log_p_e == max_log_p:
        return 'e'
    if log_p_m == max_log_p:
        return 'm'
    

table = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))

english_stopwords = stopwords.words('english')
english_stopwords = [str(x) for x in english_stopwords]

stemmer = PorterStemmer()

p_vocabulary_given_b = train_stats.p_vocabulary_given_b
p_vocabulary_given_t = train_stats.p_vocabulary_given_t
p_vocabulary_given_e = train_stats.p_vocabulary_given_e
p_vocabulary_given_m = train_stats.p_vocabulary_given_m

total_b = train_stats.total_b
total_e = train_stats.total_e
total_t = train_stats.total_t
total_m = train_stats.total_m


f = open('newsCorpora.csv')

count_correct_b = 0
count_correct_t = 0
count_correct_e = 0
count_correct_m = 0

count_total_b = 0
count_total_t = 0
count_total_e = 0
count_total_m = 0

total_count = 0

confusion_matrix = np.zeros((4,4))
class_to_int = {'b':0,'e':1,'t':2,'m':3}

for i in f:
    temp_list = i.decode('utf-8').strip().split('\t')
    headline = temp_list[1]
    words = headline.split()
    words_cleaned = [x.translate(table).lower() for x in words]
    words_cleaned_stopwords = [stemmer.stem(x) for x in words_cleaned if x not in english_stopwords]   
    while '' in words_cleaned_stopwords:
        words_cleaned_stopwords.remove('')
    c = classify(words_cleaned_stopwords,p_vocabulary_given_m,p_vocabulary_given_t,p_vocabulary_given_e,p_vocabulary_given_b,
                 total_b,total_t, total_m,total_e)
    
    total_count += 1

    confusion_matrix[class_to_int[temp_list[4]]][class_to_int[c]] += 1
    
    if (total_count%1000)==0:
        print(confusion_matrix)
        total_count = 0


f.close()
