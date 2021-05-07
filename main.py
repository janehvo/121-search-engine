import requests
from urllib.parse import urldefrag
import json, os
from text import get_text, get_tokens
from index import inverted_index, write_remaining

INDEX_FILE = 'index.json'
document_count = 0

def get_files(root_directory):
    global document_count
    global unique_urls
    global INDEX_FILE
    f = open(INDEX_FILE, 'w')
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            path = os.path.join(subdir, file)
            # .DS_Store is a Mac thing that gets in the way sometimes....
            if 'DS_Store' not in path:
                document_count += 1
                read_file(path, f)
    
    write_remaining(f)
    f.close()


def read_file(path, file_obj):
    try:
        with open(path) as json_file:
            data = json.load(json_file)
            url = urldefrag(data['url'])[0]
            content = data['content']
            acquire_text(url, content, file_obj)
    except FileNotFoundError:
        print('file does not exist')
        return


def acquire_text(url, content, file_obj):
    global index_file
    data = get_text(content)
    inverted_index(url, data, file_obj)


def get_document_count():
    global document_count
    return document_count


if __name__ == "__main__":
    # get_files('/Users/jane/Desktop/ANALYST')
    get_files('/Users/jane/Desktop/corpus')
    print('document count: ', get_document_count())
    print('unique tokens', get_tokens())
