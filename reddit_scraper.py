#new line for each comment?
#make callable from another script?
#gather all comments?
#refacter - namely retrieve_db() and get_data()
#URLS ARE MAKING IT THROUGH AGAIN, WTF

import re
import pickle
import praw

#Below could be refactered for clarity
def retrieve_db(groupings, n_samples):

    pickle_lists = []
    i = 0

    for path_list in groupings:

        pickle_lists.append([])

        for subR in path_list:

            loc_path = subR + '.pickle'

            try:
                pickle = open_data(loc_path)
                pickle_lists[i].append(pickle)

                print(loc_path + ' found')

            except OSError:
                save_data(loc_path, subR, n_samples)

                pickle = open_data(loc_path)
                pickle_lists[i].append(pickle)

                print(loc_path + ' saved')

        i += 1

    return pickle_lists

#Bellow code returns error because for some reason it doesn't open the file as a list
def open_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f) #refactor this after testing
        return data

def save_data(path, subR, n_samples):
    with open(path, 'wb') as f:
        data = get_data(subR, n_samples)
        pickle.dump(data, f)#, pickle.HIGHEST_PROTOCOL       #Refactor this as well

        print(len(data), ' comments found from ', subR)

def get_data(subR, n_samples):
    count = 0
    data = []
    reddit = authenticate()
    posts = reddit.subreddit(subR).hot(limit = 1000) #1000 is max, use 1 - 10 for testing

    #iterates through first layer of replies to every comment to every collected post, and checks for varius conditions
    for post in posts:
        post.comments.replace_more(limit = 32) #requests and replaces up to 32 unloaded comments, remainder are removed
        for comment in post.comments:
            if count < n_samples:
                com_str = clean_str(comment.body)
                if (com_str != '' and com_str != 'removed' and 'i am a bot' not in com_str):
                    data.append(com_str)
                    count += 1

                #could make this a different function so that its a little more ledgibel,
                #could also put most of the below and above logic in it to minimize duplicate data
                #Or could just use Adrian's refactoring - prolly do that
                for reply in comment.replies:
                    if count < n_samples:
                        reply_str = clean_str(reply.body)
                        if (reply_str != '' and reply_str != 'removed' and 'i am a bot' not in reply_str):
                            data.append(reply_str)
                            count += 1
                    else:
                        return data
            else:
                return data

    print('___WARNING,_ONLY_', count, '_COMMENTS_WERE_DISCOVERED_IN_', subR)
    return data

def authenticate():
    #returns authenticated instance of reddit
    reddit = praw.Reddit(
        client_id = "WR8P3Z6eTfMnm881Gn-lmw",
        client_secret = "cFQfdkbzdxZBx-rIGATE0zkYaNRH5w",
        password = "X5^Sxz^$-cT5eVH",
        user_agent = "Web Scraper for Personal ML Project 0.1 by /u/decentcelebration501",
        username = "decentcelebration501",
    )
    return reddit

def clean_str(string):
    string = re.sub(r'http\S+', '', string)#removes urls
    string = string.lower()#converts to lowercase

    #put something to handle r/subbRedditReference here?

    #seperates words that appear at the begining and end of sentences
    string = string.replace('.', ' ')
    string = string.replace('!', ' ')
    string = string.replace('?', ' ')
    string = string.replace('/', ' ')
    string = string.replace(',', ' ')#not all are gramatically correct, 
                                     #or maybe add space to the below code

    #removes any remaining special characters
    whitelist = set('abcdefghijklmnopqrstuvwxyz ')
    string = ''.join(filter(whitelist.__contains__, string))

    return string

#final_data = retrieve_db('conservative.pickle', 'conservative', 50)

#retrieve_db('liberal.csv', lib_paths, n_samples)
