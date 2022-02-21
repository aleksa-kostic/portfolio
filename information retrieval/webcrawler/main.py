import atexit
import logging

import sys

from corpus import Corpus
from crawler import Crawler
from frontier import Frontier

if __name__ == "__main__":
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # Instantiates frontier and loads the last state if exists
    frontier = Frontier()
    # frontier.load_frontier()

    # Instantiates corpus object with the given cmd arg
    corpus = Corpus(sys.argv[1])
    print(sys.argv[1])
    print('Corpus instantiated.')
    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    atexit.register(frontier.save_frontier)

    # Instantiates a crawler object and starts crawling
    crawler = Crawler(frontier, corpus)
    print('Crawling...')
    crawler.start_crawling()

    # ANALYTICS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # SUBDOMAINS COUNTS
    _subdomains = crawler.subdomains

    # PAGE WITH MOST VALID OUT LINKS
    _mostValidOutlinks = [key for key, value in crawler.count_valid_links.items() if
                          value == max(crawler.count_valid_links.values())]
    if len(_mostValidOutlinks) == 1:
        _mostValidOutlinks = _mostValidOutlinks[0]

    # IDENTIFIED TRAPS
    _identifiedTraps = crawler.identified_traps

    # LONGEST PAGE
    _longestPage = [key for key, value in crawler.page_word_count.items() if
                    value == max(crawler.page_word_count.values())]
    if len(_longestPage) == 1:
        _longestPage = _longestPage[0]

    # FIFTY (50) MOST COMMON WORDS
    _frequenciesSorted = sorted(crawler.word_frequencies.items(), key=lambda x: x[1], reverse=True)[:50]
    _fiftyMostFrequent = _frequenciesSorted[:50]

    print(_subdomains, '\n',
          _mostValidOutlinks, '\n',
          _identifiedTraps, '\n',
          _longestPage, '\n',
          _fiftyMostFrequent)
