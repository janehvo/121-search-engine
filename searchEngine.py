from nltk import PorterStemmer
import re, json, time


# split the query string if it is a phrase
# for each term in the query
#   get its first character, then open the respective index file.
#   get the postings for the term
#   rank the document based on the postings
#   add the document to a dict with its score, sorted by score
# return the top 10 results (by score)


def retrieve_query(query:str):
    try:
        term_results = []
        stemmer = PorterStemmer()
        # SPLLIT AND TOKENIZE QUERY
        # get rid of any punctuation in query
        query = re.sub("[^0-9a-zA-Z]+", " ", query)

        for term in query.split():
            term = stemmer.stem(term)
            marker = term[0]
            filename = 'index/' + marker + '.txt'
            with open(filename) as index:
                postings = json.load(index)[term]
                term_results.append(rank(postings))
                postings.clear()
            index.close()

        result = merge_results(term_results)

        print('\nSEARCH RESULTS')
        for r in get_results(result):
            print(r)
    except KeyError:
        print("Sorry, there were no pages matching your request.")


def rank(postings:list):
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

    return ranked


def merge_results(results:list):
    results = sorted(results, key = len)
    merged = results[0]
    for result in results[1:]:
        for doc in result:
            if doc in merged:
                merged[doc] += result[doc]
            else:
                merged[doc] = result[doc]

    return merged


def get_results(posting:dict)->list:
    top10 = sorted(posting.keys(), key = lambda score : posting[score], reverse=True)[0:10]
    f = open('map.json')
    docID_map = json.load(f)
    urls = [docID_map[str(id)] for id in top10]
    docID_map.clear()
    return urls


if __name__ == "__main__":
    query = input('what would you like to search?\n')
    start = time.time()
    retrieve_query(query)

    print("TIME TO RETRIEVE QUERY: ", str(time.time() - start), "seconds")
