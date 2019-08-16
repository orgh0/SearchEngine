import re
import argparse
from collections import *
import tqdm as tqdm

from utils import get_context, update_words

index_categories = ['title', 'text', 'category', 'infobox']

pagination_val  = 10

def make_index(iter_doc):
    num_pages = 0
    output_file_num = 0
    index_dict = dict()

    for cat in index_categories:
        index_dict[cat] = defaultdict(list)
    
    for event, elem in tqdm.tqdm(iter_doc):
        tag =  re.sub(r"{.*}", "", elem.tag)
        # print("Tag:", tag)
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
                    categories = re.findall("\[\[Category:(.*?)\]\]", text)
                    update_words(word_dict["category"], categories)
                
                    infoboxes = re.findall("{{Infobox([\s\S]*)}}", text)
                    update_words(word_dict["infobox"], infoboxes)
                except:
                    pass

                try:
                    text = text.lower()
                    update_words(word_dict["text"], text, istext=True)
                except:
                    pass
            if tag == "title":
                text = elem.text
                try:
                    text = text.lower()
                    title = text+"\n"
                    update_words(word_dict["title"], text, istext=True)
                except:
                    pass
            if tag == "page":
                index = "d"+str(num_pages)
                print("Len of cat", len(word_dict["category"]))
                print("Len of text", len(word_dict["text"]))
                print("Len of title", len(word_dict["title"]))
                print("Len of infobox", len(word_dict["infobox"]))
                for key, value in word_dict.items():
                    for word in value:
                        s = index + "->" + str(value[word])
                        index_dict[key][word].append(s)

                if num_pages % pagination_val == 0:
                    for key, value in index_dict.items():
                        # print(key)
                        # print(value)
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
