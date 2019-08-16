import re
import argparse
from collections import *

from utils import get_context, update_words

index_categories = ['title', 'text', 'category', 'infobox']
title_tags = open("./data/title_tags.txt", "w")

pagination_val  = 1000

def make_index(iter_doc):
    num_pages = 0
    output_file_num = 0
    index_dict = dict()

    for cat in index_categories:
        index_dict[cat] = defaultdict(list)
    
    for event, elem in iter_doc:
        tag =  re.sub(r"{.*}", "", elem.tag)
        if event == "start":
            if tag == "page":
                num_pages += 1
                word_dict = dict()
                for item in index_categories:
                    word_dict[item] = {}
        if event == "end":
            if tag == "text":
                text = elem.text
                try:
                    text = text.encode("utf-8")
                    update_words(word_dict["text"], text)
                except:
                    pass
                try:
                    categories = re.findall("\[\[Category:(.*?)\]\]", text)
                    update_words(word_dict["category"], categories)
                except:
                    pass
                try:
                    infoboxes = re.findall("{{Infobox(.*?)}}", text)
                    update_words(word_dict["infobox"], text)
                except:
                    pass
            if tag == "title":
                text = elem.text
                try:
                    text = text.encode("utf-8")
                    title = text+"\n"
                    update_words(word_dict["title"], text)
                except:
                    pass
            if tag == "page":
                index = "d"+str(num_pages)
                for key, value in word_dict.items():
                    for word in value:
                        s = index + "->" + str(value[word])
                        index_dict[key][word].append(s)

                if num_pages % pagination_val == 0:
                    for key, value in index_dict.items():
                        print(key)
                        print(value)
                        file = "./output/"+key[0:2]+str(output_file_num)+".txt"
                        o = open(file, "w")
                        for word in sorted(value):
                            index = ",".join(value[word])
                            index = word + "-" + index + "\n"
                            o.write(index)
                    o.close()
                    output_file_num += 1
                    for key, val in index_dict.items():
                        index_dict[key].clear()
            elem.clear()
     
def main(data, output_dep_folder):
    iter_doc = get_context(data)
    make_index(iter_doc)

if __name__ == '__main__':

        parser = argparse.ArgumentParser()

        ## Required parameters
        parser.add_argument("-i","--data",default=None, type=str, required=True)
        parser.add_argument("-o","--output_dep_folder", default=None, type=str,required=True)

        args = parser.parse_args()

        main(data=args.data, output_dep_folder=args.output_dep_folder)
