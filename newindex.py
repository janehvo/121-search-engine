# script to create partial indexes
# PARTIAL INDEX STRUCTURE:
#   { term: [
#       {docID: _, tfidf: _, html: []}
#   ]]}

import json, os, sys, re
from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from mergeIndex import set_doc_count, create_index

INDEX_FILE = 'index.json'
document_count = 0
docID = 1
url_id_map = {}
unique_tokens = set()
index = defaultdict(list)
partial = 0


def create_partial_indexes(root_directory):
    global document_count
    global INDEX_FILE
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
                        url_id_map[docID] = data['url']

                        # get text in file and create index
                        data = get_postings(docID, data['content'])
                        write_to_partial()
                        # change docID for every document
                        docID += 1
                except FileNotFoundError:
                    print('file does not exist')
                    continue
    write_remaining()


def get_postings(docID, content):
    global unique_tokens
    global index

    stemmer = PorterStemmer()
    term_freq = defaultdict(int)
    html = defaultdict(set)
    word_count = 0

    # using lxml to parse is good for broken html
    soup = BeautifulSoup(content, 'html.parser')
    # find important html tags in text
    html = get_html(soup)
    # tokenize entire document
    for token in soup.get_text().split():
        if token != "":
            word_count += 1
            unique_tokens.add(token)    # unique tokens regardless of stem (?)
            term_freq[stemmer.stem(token)] += 1

    for token in term_freq:
        # calculating TF (term frequency) for terms in document
        # will be useful later for calculating tfIDF
        norm_tf = term_freq[token]/word_count
        text_importance = []
        try:
            text_importance = html[token]
        except KeyError:
            continue
        # replace any punctuation in the token
        token = re.sub("[^0-9a-zA-Z]+", "", token)
        # add to partial index
        posting = {'docID':docID, 'tf-idf':norm_tf, 'html': text_importance}
        index[token].append(posting)


def get_html(soup)->defaultdict(list):
    stemmer = PorterStemmer()
    html = defaultdict(set)

    # get title tags
    title = soup.find_all('title')  # 4
    for t in title:
        text = t.get_text().split()
        for word in text:
            html[stemmer.stem(word)].add('title')

    # get h1-h3 tags
    h_major = soup.find_all(['h1', 'h2', 'h3']) # 3
    for h in h_major:
        text = h.get_text().split()
        for word in text:
            html[stemmer.stem(word)].add('hMajor')

    # get h4-h6 tags
    h_minor = soup.find_all(['h4', 'h5', 'h6']) # 2
    for h in h_minor:
        text = h.get_text().split()
        for word in text:
            html[stemmer.stem(word)].add('hMinor')

    # get b and strong tags
    bold = soup.find_all(['b', 'strong'])   # 1
    for b in bold:
        text = b.get_text().split()
        for word in text:
            html[stemmer.stem(word)].add('bold')

    return {token:list(postings) for token, postings in html.items()}


def write_to_partial():
    global partial
    # write partial index to file if the partial index is 100mb
    size = sys.getsizeof(index)
    print(size)
    # if size > 100000000:
    if size > 100000:
        filename = 'partials/index' + str(partial) + '.json'
        partial_index = open(filename, 'w')
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

    # CREATE PARTIAL INDEXES
    create_partial_indexes('/Users/jane/Desktop/ANALYST')
    get_stats()

    # MERGE PARTIAL INDEX
    set_doc_count(document_count)   # used for idf
