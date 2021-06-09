from nltk import PorterStemmer
import re, json, time

STOPWORDS = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there',
            'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be',
            'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off',
            'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below',
            'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself',
            'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
            'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in',
            'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can',
            'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
            'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing',
            'it', 'how', 'further', 'was', 'here', 'than']

def retrieve_query(query:str):
    '''Given a query string, display the top 10 results.'''
    global STOPWORDS

    start = time.time()

    try:
        term_results = []
        stemmer = PorterStemmer()

        # FILTERING QUERY
        # strip all punctuation from the query, leaving only alphanumeric chars and spaces
        query = re.sub("[^0-9a-zA-Z ]+", "", query)
        # remove duplicate words
        query = list(set(term for term in query.split() if term not in STOPWORDS))
        print(query)

        for term in query:
            term = stemmer.stem(term)
            marker = term[0]

            position = get_position(marker, term)

            postings = get_postings(marker, term, position)

            term_results.append(rank(postings))

            postings.clear()

        result = merge_results(term_results)

        print('\nSEARCH RESULTS')
        for r in get_top_results(result):
            print(r)
        
        print("TIME TO RETRIEVE QUERY: ", str(time.time() - start), "seconds")

        return get_top_results(result)

    except KeyError:
        #print("Sorry, there were no pages matching your request.")
        return []


def get_position(marker, term)->int:
    '''Access the index of the index to return term position.'''
    filename = 'indexOfIndex/' + marker + '.txt'
    f = open(filename, 'r')
    positions = json.load(f)
    position = positions[term]
    positions.clear()
    return position


def get_postings(marker, term, position)->list:
    '''Return term postings.'''
    s = time.time()

    filename = 'index/' + marker + '.txt'
    index = open(filename)
    index.seek(position)

    posting = index.readline()
    posting = eval(posting)
    if type(posting) == tuple:
        posting = posting[0]

    print('retrieval time: ', str(time.time() - s))

    p = posting[term]
    posting.clear()

    return p


def rank(postings:list)->dict:
    '''Give a ranking (score) to each document.'''
    s = time.time()
    ranked = dict()

    for posting in postings:
        score = posting['tf-idf']
        html = posting['html']
        if html != 0:
            if 'title' in html:
                score += 0.3
            if 'hMajor' in html:
                score += .25
            if 'hMinor' in html:
                score += 0.2
            if 'bold' in html:
                score += 0.15
        ranked[posting['docID']] = score
    print('ranking time: ', str(time.time() - s))

    return ranked


def merge_results(results:list)->list:
    '''Merge all documents that match the query.'''
    s = time.time()
    results = sorted(results, key = len)
    merged = results[0]
    for result in results[1:]:
        for doc in result:
            if doc in merged:
                merged[doc] += result[doc]
            else:
                merged[doc] = result[doc]
    print('merging time: ', str(time.time() - s))
    return merged


def get_top_results(posting:dict)->list:
    '''Return top 10 results from all results.'''
    top10 = sorted(posting.keys(), key = lambda score : posting[score], reverse=True)[0:10]
    f = open('map.json')
    docID_map = json.load(f)
    urls = [docID_map[str(id)] for id in top10]
    docID_map.clear()
    return urls


if __name__ == "__main__":
    query = input('what would you like to search?\n')

    retrieve_query(query)
