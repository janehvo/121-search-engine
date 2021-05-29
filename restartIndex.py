from os import listdir

def reset_index():
    for index in listdir('index'):
        path = 'index/' + index
        f = open(path, 'w+')
        f.write('[]')
        f.close()