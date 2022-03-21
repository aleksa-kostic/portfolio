from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import sqlalchemy
import nltk
import re
import os
from tqdm import tqdm
import multiprocessing


def get_wordnet_pos(treebank_tag):
    '''
        Converts treebank tags to Wordnet POS names.

        Whole function (modified): Suzana
        https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python

        RESOURCE
        All possible tags : https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
    '''

    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'  # treat token as noun.


def removeStopwords(word_list):
    '''
        Removes English stopwords from a list of words.
        List comprehension done by : Daren Thomas
        https://stackoverflow.com/questions/5486337/how-to-remove-stop-words-using-nltk-or-python
    '''

    return [word for word in word_list if word not in stopwords.words('english')]


def lemmatize(word_list):
    '''
        Lemmatizes a list of two tuples with token and a part of speech pairs.
    '''

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos=tag) for word, tag in word_list]


def clean(word_list):
    '''
        Cleans a list of words by removing stop words and applying lemmatization to each word.
    '''
    word_list = removeStopwords(word_list)  # Removing stop words
    treebank_tags = nltk.pos_tag(word_list)  # Identify parts of speech, need to simplify tags using get_pos_tag()

    wordnet_tags = []  # New list with simplified tags, not sure why this takes two steps from NLTK...

    for token, tag in treebank_tags:
        wordnet_tags.append((token, get_wordnet_pos(tag)))

    return lemmatize(wordnet_tags)  # Return lemmatized words


def getKeywords(soup):
    '''
        Gets all keywords (headers, bolded, titles, listed items) from an HTML document, these keywords are important to our search engine as they
        carry more weight than the words found in the text.

        Returns a list of keywords, empty list if there aren't any.
            Could be enhanced by giving weight to each word, e.g. Title tokens have more weight than bolded tokens

        Regex found by user phd,
        https://stackoverflow.com/questions/45062534/how-to-grab-all-headers-from-a-website-using-beautifulsoup

        HTML stripping : Jorge Galvis
        https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44

        Puncuation stripping : rmalouf
        https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer
    '''

    raw_keywords = soup.find_all(
        [re.compile('^h[1-6]$'), 'b', 'title', 'li'])  # Regex to find all keywords, see citation above.

    keywords = []

    # Stripping keyword tags
    for raw_keyword in raw_keywords:
        keyword = raw_keyword.get_text(" ", strip=True).lower().replace('\n', " ")

        tokenizer = nltk.tokenize.RegexpTokenizer(
            r'\w+\'?\w*')  # Getting rid of unnecessary punctuation (preserving apostrophes)
        keywords.extend(tokenizer.tokenize(keyword))

    return clean(keywords)


def getTokens(soup):
    '''
        Gets all tokens from html, removes stop words and lemmatizes. Returns list of tokens.
    '''

    text = soup.get_text(" ", strip=True).lower().replace('\n', " ")

    tokenizer = nltk.tokenize.RegexpTokenizer(
        r'\w+\'?\w*')  # Getting rid of unnecessary punctuation (preserving apostrophes)
    tokens = tokenizer.tokenize(text)

    return clean(tokens)


def mult_dir(dir):
    root_directory = 'C:/Users/aKost/Desktop/2021-2022/WINTER 2022/CS 121 - Information Retrieval/project3/WEBPAGES_RAW'
    engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:qrT90!xvnpc@localhost/cs121-p3')
    for file in tqdm(os.listdir(os.path.join(root_directory, dir))):  # Iterating over files
        with open(os.path.join(root_directory, dir, file), 'r', encoding="utf8") as f:  # Opening file
            f = f.read()
            soup = BeautifulSoup(f, 'html.parser')

            path = os.path.join(root_directory, dir, file)

            keywords = getKeywords(soup)  # Getting keywords
            tokens = getTokens(soup)  # Getting all text tokens

            insertTokens(tokens, path, dir, file, engine)
            insertTokens(keywords, path, dir, file, engine, isKeyword=True)

def constructIndex(root_directory):
    '''
        Gets all the html in the specified path to extract tokens and stores them in a Postgres server.
    '''
    engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:qrT90!xvnpc@localhost/cs121-p3')

    for subdir, dirs, files in os.walk(root_directory):  # Iterating over folders in WEBPAGES_RAW_TEST
        a_pool = multiprocessing.Pool()
        a_pool.map(mult_dir, dirs)

    # engine.execute("CREATE INDEX inv_idx ON Tokens USING gin(token)")


def insertTokens(tokens, full_path, dir, file, engine, isKeyword=False, frequency=1):
    for token in tokens:

        token_info = (
            token,
            isKeyword,  # isKeyword
            full_path,
            dir,
            file,
            frequency
        )

        engine.execute(
            "INSERT INTO Tokens VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (token, fullPath) DO UPDATE SET token = EXCLUDED.token, isKeyword = EXCLUDED.isKeyword, fullPath = EXCLUDED.fullPath, dir = EXCLUDED.dir, file = EXCLUDED.file, frequency = EXCLUDED.frequency + 1;",
            token_info)


if __name__ == "__main__":

    # rootdir = 'C:/Users/aKost/Desktop/2021-2022/WINTER 2022/CS 121 - Information Retrieval/project3/WEBPAGES_RAW'

    # constructIndex(rootdir) 


    """
    ========================================================
    tf: term frequency of term t in doc d

    query term frequency: SUM(tf) 
        for term t 
        in query q 
        in doc d
    
    w: log frequency weight of term t in d
        if tf > 0:
            1 + log10(tf)
        else:
            0

    score for document-query pair:
        Score(q,d) = SUM(1 + log10(tf)) for term in query-document
        * score is 0 if none of the query terms is present in the document

    document frequency of term t:
        df: number of documents that contain t
    
    inverse document frequency of term t:
        idf = log10( N / df )

    ========================================================
    IMPORTANT STUFF:
    `tf-idf`: 
        - increases with number of occurrences within a document
        - increases with the rarity of the term in the collection

        w = [1 + log10(tf)] * log10( N / df )
    
    score for doc-query pair given idf:
        Score(q,d) = SUM(`tf-idf`) for term t in doc-query pair


    """

    tf_idf = dict() 

    N = 37431   # the number of docs 37431
    tokens = list()
    for i in range(N):
        tokens = processed_text[i] # return all tokens (unique) from that document
        counter = Counter(tokens + processed_title[i])
        for token in np.unique(tokens):
            tf = counter[token]/words_count     # proportion of that token in the document
            df = doc_freq(token)    # adding up the frequencies across all documents
            idf = np.log(N/(df+1)) 
            tf_idf[(doc, token)] = tf*idf

    def matching_score(query):
        query_weights = dict()
        for key in tf_idf: 
            if key[1] in tokens: # if token is in tokens
                query_weights[key[0]] += tf_idf[key] # query weights at document = tf_dif at (doc, token)
