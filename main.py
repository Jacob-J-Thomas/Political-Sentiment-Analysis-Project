#create a bag of words
#       -prevent useless words from appearing in bag of words
#create a system of vectors associated with each word
#train the model on 50% to 80% the data
#test the model on the other 50% to 20%

#https://www.projectpro.io/recipes/build-simple-neural-network-tensorflow
#https://www.youtube.com/watch?v=Go-MHJyGzPg

import reddit_scraper
import numpy as np
#import tensorflow as tf
#from tensorflow import keras
import nltk
#nltk.download('wordnet')#only need to run this once
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer#replace with stemming if you decide context is important later -- PorterStemmer
from nltk.corpus import wordnet

n_samples = 10
c_data = []
l_data = []
paths = ['Conservative',
         'Republican',
         'Liberal',
         'Democrats']

#Could we make the retrieve_db() function work so that it handles the below logic,
# and accepts n number of "path in paths" and n number groups of "paths" all together?
for path in paths:
    loc_path = path + '.pickle'
        
    if (path == 'Conservative') or (path == 'Republican'):
        data = reddit_scraper.retrieve_db(loc_path, path, n_samples)
        c_data.append(data)
    elif (path == 'Liberal') or (path == 'Democrats'):
        data = reddit_scraper.retrieve_db(loc_path, path, n_samples)
        l_data.append(data)
    else:
        print('Error: The specified database path, ', path, ', does not appear in any subset grouping')
    
    #we might want to move the try and except handler into this function. I believe this could allow us to access files seperately

lemmatizer = WordNetLemmatizer()

def bagify(data):

    word_bag = []

    for string in data:
        string = word_tokenize(str(string))
        #print string here to see if its being converted to a list of strings the size of words, or what
        for word in string:
            word = lemmatizer.lemmatize(word)
            if word not in word_bag:
                word_bag.append(word)
    
    return word_bag

c_bag = bagify(c_data)

printable_list = c_bag[:50]
print(printable_list)




