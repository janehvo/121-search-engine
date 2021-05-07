# methods for index creation

# inverted index
# token is the key, the value is a list that contains the urls and its frequency

from collections import defaultdict
import sys
import json


# index = {token: {url: freq, url:freq}, token: {url: freq, url: freq}}

index = defaultdict(dict)

def inverted_index(url, data, index_file):
    for token in data:
        index[token][url] = data[token]

    check_size(index_file)

def check_size(index_file):
    global index
    size = sys.getsizeof(index)
    if size > 1000000:
        print('writing')
        json.dump(index, index_file, indent=3)
        index.clear()

def write_remaining(index_file):
    global index
    json.dump(index, index_file, indent = 3)
    index.clear()
