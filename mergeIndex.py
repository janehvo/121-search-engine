# script to merge all partial indexes in /partials directory
# PARTIAL INDEX STRUCTURE:
#   { term: [
#       {docID: _, tfidf: _, html: []}
#   ]]}

# outline of what i plan to do:
#   first, output every term into a corresponding alphabetized file
#       - read a partial index item by item
#       - write that item into a file corresponding to the first character of the token
#       - open and close the file each time
#   once that's done, merge the files into a large index (perhaps using object merge?)


import json
from json.decoder import JSONDecodeError
from os import listdir
from jsonmerge import merge
from math import log


DOC_COUNT = 1988

def set_doc_count(count):
    global DOC_COUNT
    DOC_COUNT = count


def create_index():
    global DOC_COUNT
    for partial in listdir('partials'):
        file_path = 'partials/' + partial
        partial_index = open(file_path)
        pi = json.load(partial_index)

        write_to_disk(pi)


# write to alphabetized files
# all files will be in the index, which is a fodler
def write_to_disk(partial_index):
    filename = 'index/1.txt'
    f = open(filename, 'a+')    # allows for read and write
    try:
        final = json.load(f)
    except JSONDecodeError:
        final = {}

    for term in partial_index:
        # first character for alphabetization 
        if term != '':
            char = term[0]
            char_file = 'index/' + char + '.txt'
            if char_file != filename:
                # update the open file (this will go in order of the characters)
                f.seek(0)
                f.truncate()
                # calculate tf-idf scores 
                add_tfIDF(final)
                json.dump(final, f, indent=3)
                # now close the file, since we're done writing to the file
                f.close()
                final.clear()

                # open a new file with the correct corresponding character marker
                f = open(char_file, 'a+')
                try:
                    final = json.load(f)
                except JSONDecodeError:
                    final = {}

            if term in final:
                # merge the two dictionaries together
                final[term] = merge(final[term], partial_index[term])
            else:
                final[term] = partial_index[term]


# modify the postings in place to include tf-idf
def add_tfIDF(index:dict):
    global DOC_COUNT
    for term in index:
        idf = log(DOC_COUNT / len(term))
        for posting in index[term]:
            tf = posting['tf-idf']
            print(tf * idf)
            posting['tf-idf'] = tf * idf


if __name__ == "__main__":
    create_index()