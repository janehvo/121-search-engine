# script to create partial indexes
# PARTIAL INDEX STRUCTURE:
#   { term: {
#       document: [
#           tf (float), [html_tags (list of strings)]
#   ]}}

import json, os, sys
from urllib.parse import urldefrag
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

document_count = 0
docID = 1
url_id_map = {}
unique_tokens = set()
index = defaultdict(dict)
partial = 0

def get_files(root_directory):
    global document_count
    global docID

    for subdir, _, files in os.walk(root_directory):
        for file in files:
            path = os.path.join(subdir, file)
            # .DS_Store is a Mac thing that gets in the way sometimes....
            if 'DS_Store' not in path:
                document_count += 1
                try:
                    # read the file
                    with open(path) as json_file:
                        data = json.load(json_file)
                        # mapping the docID to the document
                        url = urldefrag(data['url'])[0]
                        url_id_map[docID] = url

                        # get text in file and create index
                        content = data['content']
                        data = get_text(docID, content)
                        inverted_index(docID, data)
                        # change docID for every document
                        docID += 1
                except FileNotFoundError:
                    print('file does not exist')
                    return

    write_remaining()
    get_stats()


def get_text(docID, content):
    global unique_tokens

    stemmer = PorterStemmer()
    postings = defaultdict(int)
    word_count = 0

    # using lxml to parse is good for broken html
    soup = BeautifulSoup(content, 'html.parser')

    for token in soup.get_text().split():
        word_count += 1

        unique_tokens.add(token)    # unique tokens regardless of stem (?)
        postings[stemmer.stem(token).lower()] += 1

    return postings, word_count


def inverted_index(docID, data):
    global index
    global partial

    for token in data[0]:
        # calculating TF (term frequency) for terms in document
        # will be useful later for calculating tfIDF
        norm_tf = data[0][token]/data[1]
        index[token][docID] = norm_tf

    # write partial index to file if the partial index is 100mb
    size = sys.getsizeof(index)
    print(size)
    # if size > 100000000:
    if size > 1000000:
        filename = 'partials/index' + str(partial) + '.json'
        partial_index = open(filename, 'a+')
        print('writing to', filename)

        sorted_index = {k:v for k, v in sorted(index.items(), key=lambda item: item[0])}
        json.dump(sorted_index, partial_index, indent=1)
        index.clear()
        partial_index.close()
        partial += 1
        

def write_remaining():
    global index
    global url_id_map

    # write document ID map to a file
    id_map = open('map.json', 'w')
    json.dump(url_id_map, id_map, indent = 3)
    url_id_map.clear()
    id_map.close()

    # write the remaining partial index to a file
    sorted_index = {k:v for k, v in sorted(index.items(), key=lambda item: item[0])}
    filename = 'partials/index' + str(partial) + '.json'
    partial_index = open(filename, 'w')
    json.dump(sorted_index, partial_index, indent=3)
    index.clear()
    partial_index.close()


def get_stats():
    global document_count
    global unique_tokens

    print('document count: ', document_count)
    print('unique tokens', len(unique_tokens))


if __name__ == "__main__":
    print('START')
    get_files('/Users/jane/Desktop/ANALYST')
