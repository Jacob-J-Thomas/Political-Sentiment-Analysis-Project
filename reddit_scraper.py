#new line for each comment?
#make callable from another script?
#gather all comments?
#refacter

#import cleantext
import re
import pickle
import praw

def retrieve_db(loc_path, subR, n_samples):
    try:
        data = open_data(loc_path)
        print(loc_path + ' found')
            
        return data

    except OSError:
        save_data(loc_path, subR, n_samples)

        data = open_data(loc_path)
        print(loc_path + ' saved')

        return data

def open_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
        return data

def save_data(path, subR, n_samples):
    with open(path, 'wb') as f:
        data = get_data(subR, n_samples)
        print(len(data), ' comments found from ', subR)
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

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

    #seperates words that appear at the begining and end of sentences
    string = string.replace('.', ' ')
    string = string.replace('!', ' ')
    string = string.replace('?', ' ')

    #removes any remaining special characters
    whitelist = set('abcdefghijklmnopqrstuvwxyz ')
    cleaned = ''.join(filter(whitelist.__contains__, string))#removes all other special characters
                
    return cleaned

#retrieve_db('cons.csv', con_paths, n_samples)
#retrieve_db('liberal.csv', lib_paths, n_samples)
