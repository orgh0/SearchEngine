import re

import xml.etree.cElementTree as em

alphabet_selector = re.compile("[^a-zA-Z]")

def update_words(word_dict, entry):
    if entry:
        for string in entry:
            string_list = re.split(alphabet_selector, string)
            for word in string_list:
                word = stem_word(word.lower())
                if word:
                    if word not in stop_words:
                        if word not in word_dict:
                            word_dict[word] = 0
                        word_dict[word] += 1

def get_context(data):
    context = em.iterparse(data, events=("start", "end"))
    context = iter(context)
    return context
