import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer  

stop_words = set(stopwords.words('english'))

import xml.etree.cElementTree as em

alphabet_selector = re.compile("[^a-zA-Z]")

ps = PorterStemmer() 

def update_words(word_dict, entry, istext=False):
    if istext:
        entry = re.split(alphabet_selector, entry)
    else:
        pass
    if entry:
        for item in entry:
            string_list = re.split(alphabet_selector, item)
            for word in string_list:
                word = ps.stem(word.lower())
                if word:
                    if word not in stop_words:
                        if word not in word_dict:
                            word_dict[word] = 0
                        word_dict[word] += 1
                else:
                    pass

def get_context(data):
    context = em.iterparse(data, events=("start", "end"))
    context = iter(context)
    return context
