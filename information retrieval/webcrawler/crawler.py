import logging
import re

# import lxml.html
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag

logger = logging.getLogger(__name__)


class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus):
        self.frontier = frontier
        self.corpus = corpus
        self.invalid_urls = set()
        self.invalid_count = 0
        self.directories_dict = dict()
        self.subdomains = dict()
        self.count_valid_links = dict()
        self.identified_traps = list()
        self.page_word_count = dict()  # NOT FREQUENCIES
        self.word_frequencies = dict()  # FREQUENCIES

        self._STOPWORDS = ["<!--...-->",
                           "<!DOCTYPE>",
                           "<a>",
                           "<abbr>",
                           "<acronym>",
                           "<address>",
                           "<applet>",
                           "<area>",
                           "<article>",
                           "<aside>",
                           "<audio>",
                           "<b>",
                           "<base>",
                           "<basefont>",
                           "<bdi>",
                           "<bdo>",
                           "<big>",
                           "<blockquote>",
                           "<body>",
                           "<br>",
                           "<button>",
                           "<canvas>",
                           "<caption>",
                           "<center>",
                           "<cite>",
                           "<code>",
                           "<col>",
                           "<colgroup>",
                           "<data>",
                           "<datalist>",
                           "<dd>",
                           "<del>",
                           "<details>",
                           "<dfn>",
                           "<dialog>",
                           "<dir>",
                           "<div>",
                           "<dl>",
                           "<dt>",
                           "<em>",
                           "<embed>",
                           "<fieldset>",
                           "<figcaption",
                           "<figure>",
                           "<font>",
                           "<footer>",
                           "<form>",
                           "<frame>",
                           "<frameset>",
                           "<h1>",
                           "<h2>",
                           "<h3>",
                           "<h4>",
                           "<h5>",
                           "<h6>",
                           "<head>",
                           "<header>",
                           "<hr>",
                           "<html>",
                           "<i>",
                           "<iframe>",
                           "<img>",
                           "<input>",
                           "<ins>",
                           "<kbd>",
                           "<label>",
                           "<legend>",
                           "<li>",
                           "<link>",
                           "<main>",
                           "<map>",
                           "<mark>",
                           "<meta>",
                           "<meter>",
                           "<nav>",
                           "<noframes>",
                           "<noscript>",
                           "<object>",
                           "<ol>",
                           "<optgroup>",
                           "<option>",
                           "<output>",
                           "<p>",
                           "<param>",
                           "<picture>",
                           "<pre>",
                           "<progress>",
                           "<q>",
                           "<rp>",
                           "<rt>",
                           "<ruby>",
                           "<s>",
                           "<samp>",
                           "<script>",
                           "<section>",
                           "<select>",
                           "<small>",
                           "<source>",
                           "<span>",
                           "<strike>",
                           "<strong>",
                           "<style>",
                           "<sub>",
                           "<summary>",
                           "<sup>",
                           "<svg>",
                           "<table>",
                           "<tbody>",
                           "<td>",
                           "<template>",
                           "<textarea>",
                           "<tfoot>",
                           "<th>",
                           "<thead>",
                           "<time>",
                           "<title>",
                           "<tr>",
                           "<track>",
                           "<tt>",
                           "<u>",
                           "<ul>",
                           "<var>",
                           "<video>",
                           "<wbr>",
                           "a",
                           "about",
                           "above",
                           "after",
                           "again",
                           "against",
                           "all",
                           "am",
                           "an",
                           "and",
                           "any",
                           "are",
                           "aren't",
                           "as",
                           "at",
                           "be",
                           "because",
                           "been",
                           "before",
                           "being",
                           "below",
                           "between",
                           "both",
                           "but",
                           "by",
                           "can't",
                           "cannot",
                           "could",
                           "couldn't",
                           "did",
                           "didn't",
                           "do",
                           "does",
                           "doesn't",
                           "doing",
                           "don't",
                           "down",
                           "during",
                           "each",
                           "few",
                           "for",
                           "from",
                           "further",
                           "had",
                           "hadn't",
                           "has",
                           "hasn't",
                           "have",
                           "haven't",
                           "having",
                           "he",
                           "he'd",
                           "he'll",
                           "he's",
                           "her",
                           "here",
                           "here's",
                           "hers",
                           "herself",
                           "him",
                           "himself",
                           "his",
                           "how",
                           "how's",
                           "i",
                           "i'd",
                           "i'll",
                           "i'm",
                           "i've",
                           "if",
                           "in",
                           "into",
                           "is",
                           "isn't",
                           "it",
                           "it's",
                           "its",
                           "itself",
                           "let's",
                           "me",
                           "more",
                           "most",
                           "mustn't",
                           "my",
                           "myself",
                           "no",
                           "nor",
                           "not",
                           "of",
                           "off",
                           "on",
                           "once",
                           "only",
                           "or",
                           "other",
                           "ought",
                           "our",
                           "ours", "ourselves",
                           "out",
                           "over",
                           "own",
                           "same",
                           "shan't",
                           "she",
                           "she'd",
                           "she'll",
                           "she's",
                           "should",
                           "shouldn't",
                           "so",
                           "some",
                           "such",
                           "than",
                           "that",
                           "that's",
                           "the",
                           "their",
                           "theirs",
                           "them",
                           "themselves",
                           "then",
                           "there",
                           "there's",
                           "these",
                           "they",
                           "they'd",
                           "they'll",
                           "they're",
                           "they've",
                           "this",
                           "those",
                           "through",
                           "to",
                           "too",
                           "under",
                           "until",
                           "up",
                           "very",
                           "was",
                           "wasn't",
                           "we",
                           "we'd",
                           "we'll",
                           "we're",
                           "we've",
                           "were",
                           "weren't",
                           "what",
                           "what's",
                           "when",
                           "when's",
                           "where",
                           "where's",
                           "which",
                           "while",
                           "who",
                           "who's",
                           "whom",
                           "why",
                           "why's",
                           "with",
                           "won't",
                           "would",
                           "wouldn't",
                           "you",
                           "you'd",
                           "you'll",
                           "you're",
                           "you've",
                           "your",
                           "yours",
                           "yourself",
                           "yourselves"]

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched,
                        len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)
        print(f'Invalid url counts : {self.invalid_count}')

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        # If no content in html, no links will be found so we skip
        if url_data['content'] == None:
            return

        # If any redirection occurs, we want the final landing page to be the home url
        if url_data['final_url'] != None:
            home_url = url_data['final_url']
        else:
            home_url = url_data['url']

        outputLinks = []

        # Making content of url readable
        soup = BeautifulSoup(url_data['content'], 'html.parser')

        # Iterate over specific tags i.e. link tags 
        for link in soup.find_all('a'):

            href = link.get('href')

            if href == None:
                continue
            elif 'http://' not in href or 'https://' not in href:
                href = urljoin(home_url, href)

            url = urldefrag(href).url
            outputLinks.append(url)

            # if self.is_valid(url):
            #     # VALID NUMBER OUTLINKS
            #
            #     if url not in self.count_valid_links[home_url]:
            #         self.count_valid_links[home_url] = 1
            #     else:
            #         self.count_valid_links[home_url] += 1
            #
            #     # TOKENIZE WORDS IN DOCUMENT
            #     doc = lxml.html.fromstring(url_data['url_content'])
            #     split_content = doc.split()
            #     old_list = split_content
            #
            #     characters = '!@#$%^&*()_+={}|[]\:";?,./“”—﻿'
            #
            #     for ch in characters:
            #         new_list = list()
            #
            #         for i in range(len(old_list)):
            #             temp = old_list[i].split(ch)
            #
            #             if len(temp) == 1:
            #                 new_list.append(temp[0])
            #
            #             elif len(temp) > 1:
            #                 for j in temp:
            #                     if j != '':
            #                         new_list.append(j)
            #
            #         del old_list
            #         old_list = new_list
            #
            #     for word in self._STOPWORDS:
            #         if word in old_list:
            #             old_list.remove(word)
            #
            #     self.page_word_count[url] = len(old_list)
            #
            #     # WORD FREQUENCIES
            #
            #     for wd in old_list:
            #         if wd in self.word_frequencies:
            #             self.word_frequencies[wd] += 1
            #         else:
            #             self.word_frequencies[wd] = 1

        return outputLinks

    def has_valid_characters(self, url):
        '''
        According to RFC 3986, Section 2, characters must be, "based on the US-ASCII coded character set".
        https://stackoverflow.com/questions/7109143/what-characters-are-valid-in-a-url
        https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers 2000 character limit
        '''

        regex = r"^[A-Za-z0-9._\-~:/?#\[\]@!$&'()*+;%,=]{1,2000}$"
        r = re.compile(regex)

        return bool(re.match(r, url))

    def valid_query(self, query):
        if query.count("=") >= 6:
            return False

        return True

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """

        try:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"}:
                self.invalid_count += 1
                self.invalid_urls.add(url)
                return False

            if not self.valid_query(parsed.query):
                self.invalid_count += 1
                self.invalid_urls.add(url)
                return False

            if not self.has_valid_characters(url):
                self.invalid_count += 1
                self.invalid_urls.add(url)
                return False

            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print(f"TypeError for url in parsed(url): parsed({url})")
            self.invalid_count += 1
            self.invalid_urls.add(url)
            return False
