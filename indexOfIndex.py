# INDEX OF INDEX STRUCTURE
# {
#   term: position,
#   term: position
# }
# =========================

import json
from os import listdir

def map_posting_positions():
    positions = {}

    for index in listdir('index'):
        temp = 'index/' + index
        print(temp)
        index_file = open(temp, 'r')    # we only want to read the index
        temp = 'indexOfIndex/' + index
        index_of_index_file = open(temp, 'w')
        term = index_file.readline()

        while index_file:
            position = index_file.tell()
            term = index_file.readline()
            # end of file
            if term == ']':
                break
            else:
                # eval() returns a tuple for lines that have a comma at the end
                posting = eval(term)
                word = ''
                if type(posting) == tuple:
                    key = posting[0].keys()
                    for k in key:
                        word = k
                elif type(posting) == dict:
                    word = posting.keys()
                    for k in key:
                        word = k

                positions[word] = position


        json.dump(positions, index_of_index_file, indent=2)

        positions.clear()
        index_file.close()
        index_of_index_file.close()
