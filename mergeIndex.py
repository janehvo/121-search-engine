# script to merge all partial indexes in /partials directory
# ===================================
# PARTIAL INDEX STRUCTURE:
#   { term: [
#       {docID: _, tfidf: _, html: []},
#       {docID: _, tfidf: _, html: []}
#   ]]}
# ===================================
# FINAL INDEX STRUCTURE:
# [
#   {term: [{docID: _. tfidf: _, html: []}, {docID: -, tfidf: -, html: []}]},
#   {term: [{docID: _. tfidf: _, html: []}, {docID: -, tfidf: -, html: []}]},
#   {term: [{docID: _. tfidf: _, html: []}, {docID: -, tfidf: -, html: []}]},
# ]
# have the index as an array that we append to when loading
# if there is a similar term, just append to the postings of that term
# sorted alphabetically by term
# this way, i can readline and do seeks and tells later


import json
from os import listdir
from math import log
#from restartIndex import reset_index


DOC_COUNT = 0

def set_doc_count(count):
    global DOC_COUNT
    DOC_COUNT = count


def create_index():
    global DOC_COUNT
    # reset_index()
    
    for partial in listdir('partials'):
        file_path = 'partials/index' + partial + '.json'
        print(file_path)
        partial_index = open(file_path)
        pi = json.load(partial_index)

        write_to_disk(pi)
        pi.clear()
        partial_index.close()


# write to alphabetized files
# all files will be in the index, which is a fodler
def write_to_disk(partial_index):
    filename = 'index/0.txt'
    f = open(filename, 'r+')    # allows for read and write
    final = json.load(f)    # dict
    keys =[k for postings in final for k in postings.keys()]
    
    print(filename)

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
                f.write('[\n')
                for posting in final:
                    json.dump(posting, f)
                    if posting != final[-1]:
                        f.write(',\n')
                    else:
                        f.write('\n')
                f.write(']')
                # json.dump(final, f, indent=3)
                # now close the file, since we're done writing to the file
                f.close()
                final.clear()

                filename = char_file
                print(filename)
                
                # open a new file with the correct corresponding character marker
                f = open(char_file, 'r+')
                final = json.load(f)
                keys =[k for postings in final for k in postings.keys()]

            if term in keys:
                index = keys.index(term)
                # merge the two arrays together
                final[index][term] = final[index][term] + partial_index[term]
            else:
                final.append({term:partial_index[term]})
                keys.append(term)

    f.seek(0)
    f.truncate()
    add_tfIDF(final)
    json.dump(final, f, indent=3)
    f.close()
    final.clear()


# modify the postings in place to include tf-idf
def add_tfIDF(index:list):
    global DOC_COUNT
    for term in index:
        for posting in term:
            idf = log((DOC_COUNT / len(term[posting])), 10)
            for p in term[posting]:
                tf = p['tf-idf']
                p['tf-idf'] = (log(1+tf, 10)) * idf
