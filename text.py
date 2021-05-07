# methods for text transformation/processing
from bs4 import BeautifulSoup
import re
from collections import defaultdict

unique_tokens = set()

def get_text(content):
    global unique_tokens

    data = defaultdict(int)

    # using lxml to parse is good for broken html
    soup = BeautifulSoup(content, 'html.parser')

    sequence = re.compile(r'^[\w\d]*$')

    for token in soup.get_text().split():
        # concantenate apostrophes, then strip puncuation from the text
        token = token.replace('\'', '')
        token = re.sub(r'[^\w\s]', ' ', token)
        if re.match(sequence, token):
            unique_tokens.add(token)
            data[token.lower()] += 1

    return data


def get_tokens():
    return len(unique_tokens)
