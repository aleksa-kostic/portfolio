# main.py 
# from typing import ParamSpecArgs
from sqlalchemy import create_engine
import pandas as pd
import math
import index_constructor as ic
import nltk
import pickle
import os.path
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup


def process_one_term(t, e, n):
    """
    Calculate idf score for this term in the query

    @param t:   str(),  single term
    @param e:   sqlalchemyengine,   postgreSQL engine
    @param n:   int(),  number of documents in the corpus
    """

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

    # Document frequency: number of documents that contain t
    df = pd.DataFrame(
        e.execute(f"select count(f) from (select distinct(fullpath) from tokens where token like '{t}') as f"))

    if df.size == 0:
        idf = 0
    else:
        df = float(df[0][0])
        if df == 0 :
            idf = 0
        else:
            idf = math.log10(n / df)

    return idf


def process_multiple_terms(t_list, e, n):
    """
    If the query is more than one word long, start here

    @param t_list:  list(), query terms that were split and processed
    @param e:       sqlalchemyengine,   the postgreSQL DB engine
    @param n:       int(),  numbers of documents in the DB
    """
    processed = dict()

    for term in t_list:

        idf = process_one_term(term, e, n)
        if term not in processed.keys():
            processed[term] = idf
        else:
            continue

    return processed


def score(idfs_dict, original_query, q, e, cache):
    """
    calculate tfidf for all terms given a query

    @param idfs_dict:       dict(), dictionary of idf values for all terms in query
    @param original_query:  str(),  the original input for the search query
    @param q:               list(), split, lemmatized query
    @param e:       sqlalchemyengine,   the postgreSQL DB engine
    @param cache:           dict(), cache of query tfidf values
    """
    if original_query not in cache.keys():
        cache[original_query] = dict()
        for term in q:
            temp = pd.DataFrame(e.execute(f"select token, dir, file, frequency from tokens where token like '{term}'"))

            if temp.size == 0:
                pass
            else:
                for index, row in temp.iterrows():
                    tf = row[3]
                    tfidf = (1 + math.log10(tf)) * idfs_dict[term]
                    doc = row[1] + "/" + row[2]
                    if doc in cache[original_query].keys():
                        cache[original_query][doc] += tfidf
                    else:
                        cache[original_query][doc] = tfidf
    else:
        pass


def process_query(original_query, q, e, n, c):
    """
    Take a query and process it, then score/rank it

    @param original_query:  str(),  the original input for the search query
    @param q:               list(), split, lemmatized query
    @param e:       sqlalchemyengine,   the postgreSQL DB engine
    @param n:               int(),  number of documents in the corpus
    @param c:               dict(), previous query score/rank cache
    """
    processed = dict()

    # get the idfs
    processed = process_multiple_terms(q, e, n)

    # score the query and update the CACHE
    score(processed, original_query, q, e, c)
    # return processed


def get_body(dir):
    """
    This is for the GUI interface.
    """
    with open(os.path.join('C:/Users/aKost/Desktop/2021-2022/WINTER 2022/CS 121 - Information Retrieval/project3/WEBPAGES_RAW', dir), 'r', encoding="utf8") as f:  # Opening file
        f = f.read()

        soup = BeautifulSoup(f, 'html.parser')
        title = str()
        try:
            title = soup.find('title').string
        except:
            pass
        texts = str()
        try:
            texts = soup.get_text(" ", strip=True)
        except:
            pass

        return title, texts


if __name__ == '__main__':
    # Load the cache if it exists
    if os.path.exists("cache_pickle.txt"):
        infile = open("cache_pickle.txt",'rb')
        CACHE = pickle.load(infile)
        infile.close()
    # If a cache doesn't exist, create a new one from scratch
    else:
        CACHE = dict()
    
    engine = create_engine('postgresql://postgres:qrT90!xvnpc@localhost/cs121-p3')

    # Number of documents
    N = pd.DataFrame(engine.execute("select count(f) from (select distinct(fullpath) from tokens) as f"))
    N = float(N[0][0])

    """
    tkinter
    """
    tk = Tk()
    tk.title('CS121 - Search Engine 52')
    tk.geometry("900x775")


    """
    Functions for the GUI
    """
    def clear():
        my_entry.delete(0, END)
        my_text.delete(0.0, END)


    def retrieve(query):
        ret = str()
        query = query.lower()
        tknzr = nltk.tokenize.RegexpTokenizer(
            r'\w+\'?\w*')  # Getting rid of unnecessary punctuation (preserving apostrophes)
        tkns = tknzr.tokenize(query)

        new_query = list(set(ic.clean(tkns)))

        # get idf values for all terms in query
        process_query(query, new_query, engine, N, CACHE)

        i = 0
        for k, v in sorted(CACHE[query].items(), key=lambda item: -item[1]):
            title, texts = get_body(k)
            texts = texts[:500]
            ret += "=====================================================================\n"
            ret += f"TITLE:\t{title}\n\nLOCATION:\t{k}\n\n\n{texts}\n\n\n\n\n"
            i += 1
            if i > 20:
                break
        return ret

    def search():
        q = my_entry.get()
        clear()
        data = retrieve(q)
        my_text.insert(0.0, data)
        pass

    """
    Create the GUI layout
    """
    # Labels
    my_label_frame = LabelFrame(tk, text="Search my corpus ;~0")
    my_label_frame.pack(pady=20)

    # Format the label
    my_entry = Entry(my_label_frame, font=("Helvetica", 22), width=48)
    my_entry.pack(pady=20,padx=20)

    # create the frame
    my_frame = Frame(tk)
    my_frame.pack(pady=5)

    # scrollbar(S)
    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side=RIGHT, fill=Y)

    hor_scroll = Scrollbar(my_frame, orient='horizontal')
    hor_scroll.pack(side=BOTTOM, fill=X)

    # textbox
    my_text = Text(my_frame, yscrollcommand=text_scroll.set, wrap="none",xscrollcommand=hor_scroll.set)
    my_text.pack()

    text_scroll.config(command=my_text.yview)
    hor_scroll.config(command=my_text.xview)

    # buttons
    button_frame = Frame(tk)
    button_frame.pack(pady=10)

    search_button = Button(button_frame, text="SEARCH!!", font=('Helvetica',28),fg='#3a3a3a', command=search)
    search_button.grid(row=0, column=0, padx=20)

    clear_button = Button(button_frame, text="clear...", font=('Helvetica', 28), fg='#3a3a3a', command=clear)
    clear_button.grid(row=0, column=1, padx=20)

    # this doesn't even work
    style = ttk.Style(tk)
    style.theme_use('vista')

    # display
    tk.mainloop()

    """
    ===============================================================================================================
    After everything, save the cache and dump the pickle
    This will be used again later when the search engine is run again
    ===============================================================================================================
    """
    outfile = open("cache_pickle.txt", 'wb')
    pickle.dump(CACHE, outfile)
    outfile.close()
