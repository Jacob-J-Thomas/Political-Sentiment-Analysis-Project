#Pull commit and push
#
#create a bag of words
#   -seperate bag of words into liberal and conservative camps
#create a system of vectors associated with each word
#train the model on 50% to 80% the data
#test the model on the other 50% to 20%

import reddit_scraper
import numpy as np
#import tensorflow as tf
#from tensorflow import keras
import nltk
#nltk.download('wordnet')#only need to run these downloads once
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer#replace with stemming if you decide context is important later -- PorterStemmer
from nltk.corpus import wordnet 
from nltk.corpus import stopwords

#subreddit paths
conservative = ['conservative',
                'republican']
liberal = ['liberal',
           'democrats']

#reddit_scraper variables
n_samples = 10
groupings = [conservative,
             liberal]

data = reddit_scraper.retrieve_db(groupings, n_samples)

#Below is for testing data structure, should be as follows:
#2          - for groupings
#10         - for comments in grouping
#10         - for comments in grouping again
#2          - for groupings again
#10         - for comments in grouping again
#10         - for comments ing grouping again
for list in data:
    print('layer 1: ', len(list))
    for i in list:
        print('layer 2: ', len(i))






lemmatizer = WordNetLemmatizer()

def bagify(data):

    word_bag = []
    stop_words = set(stopwords.words('english'))#removes irrelevant words such as "i", "you", "the", "a"

    for comment in data:
        comment = word_tokenize(comment)
        #print string here to see if its being converted to a list of strings the size of words, or what
        for word in comment:
            word = lemmatizer.lemmatize(word)
            if (word not in stop_words and word not in word_bag):
                word_bag.append(word)
    
    return word_bag

#print(conservative)



# conservative = bagify(conservative)
# liberal = bagify(liberal)
# republican = bagify(republican)
# democrats = bagify(democrats)

#below are returning none for some reason - may 
# be because it is a list of lists rather than a true append
# c_bag = conservative.append(republican)
# l_bag = liberal.append(democrats)

# print(conservative)

#printable_list = c_bag[:50]
#print(printable_list)




