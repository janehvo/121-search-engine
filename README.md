# 121-search-engine

The first step is index creation. Start by running the index module (index.py).

This will first create partial indexes onto the disk.
During this partial index creation, there are postings made for each term, with each term containing the normal term frequency and an array of
strings that represent if the word is important in the text (i.e. it is a title, heading, or bold).

After that, the these partial indexes are then merged into the inverted index, where terms are sorted into according to their first character.
During this merging process, the tf-idf score is calculated for each document in each posting.

The last part of index creation is making the index of the index, which maps each term in the index to its byte position in their respective index files.


Now, the search engine is ready to be used. It can be ran via the terminal or a web interface.

To run it in the terminal, navigate to the searchEngine.py module and run it. This will prompt for a search query, which can be typed into the terminal.
To run it via the web interface, navigate to app.py and run that module. It should take you to a local server on your web browser,
where you can essentially do the same thing as the terminal version. All of the processes are the same.


The query is then processed, and the terms in query are searched for in the index.

This search happens in two main steps. First, it finds the position of the term in the index. This information is retreived from the index of the index.
The second step is using that position to retrieve the query from the index at that position. This saves time and memory. The query term's postings are retrieved.

Once all of the postings are found, they are then merged. The merge starts with the shortest posting, and merges the next posting sequentially by size.
The merged postings are then ranked, and this is done by extracting each document's tf-idf score as well as its text importance. 
Finally, once the postings are sorted by rank, the top results are retrieved. Using the document IDs of the top 10 postings, their corresponding URLs are
retrieved from the docID-url mapping.

At last, these top 10 URLs are returned to the user. 
