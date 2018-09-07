# -*- coding: utf-8 -*-
import os
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer, ToktokTokenizer
from special_characters import *


class WikiReader:
    def __init__(self, directory, tokeniser=None, char_cleaner=None, do_lower=True, count_elements=False):
        # variables for file iteration
        os_walk = list(os.walk(directory))
        if not os_walk:
            raise FileNotFoundError("os.walk(" + directory + ") was empty. Does it exist?")
        all_files = (cur_dir + "/" + f for cur_dir, _, dir_files in os_walk for f in dir_files)
        relevant_name = re.compile("wiki_[0-9]+$")
        self.filenames = sorted(filter(relevant_name.search, all_files))

        # variables for line matching inside a file
        self.WikiExtractor_doc_open = re.compile('<doc id="([0-9]+)" url="(.*)" title="(.*)">')
        self.WikiExtractor_doc_close = re.compile('</doc>')

        # tokeniser variable
        if tokeniser is None:
            self.tok = lambda sentence: sentence
        else:
            self.tok = lambda sent: tokeniser.tokenize(sent, return_str=True)

        self.do_lower = do_lower

        # variable for preparing lines for tokenisation and removing unwanted characters
        if char_cleaner is None:
            self.char_cleaner = lambda sentence: sentence
        else:
            self.char_cleaner = char_cleaner

        # additional variables for diagnostics
        self.empty_articles = []
        self.count_elements = count_elements
        self.counts = defaultdict(int)

    # matches a given line with the regexp above
    def match_xml_opening(self, xml_line):
        return self.WikiExtractor_doc_open.match(xml_line)

    # matches a given line with the regexp above
    def match_xml_closing(self, xml_line):
        return self.WikiExtractor_doc_close.match(xml_line)

    # opens a file, makes the iterator available and closes the file
    @staticmethod
    def get_file_iter(filename):
        f_handle = open(filename)
        yield from f_handle
        f_handle.close()

    # iterates over the files in the directory,
    # yielding from the iterator below
    def article_iter(self):
        for file in self.filenames:
            print('Opening ', file)
            cur_file_iter = self.get_file_iter(file)
            yield from self.single_file_iter(cur_file_iter)
        # iterated over the Wiki once, don't count in the next iterations
        self.count_elements = False

    # takes an iterator over lines from a file,
    # assuming the output format of WikiExtractor,
    # and yields the title and text of each article
    def single_file_iter(self, cur_file_iter):
        for line in cur_file_iter:
            line = line.rstrip()
            if line == "":
                continue

            open_match = self.match_xml_opening(line)
            if open_match:
                article_title = open_match.groups()[2]
            # text extraction in the else section
            # makes the iterator skip the line under the title
            # (this line is a repetition of the title)
            else:
                article_text = list(self.get_text(cur_file_iter))
                # don't yield articles with empty texts
                if article_text == []:
                    self.empty_articles.append(article_title)
                else:
                    if self.count_elements:
                        self.counts["articles"] += 1
                    yield article_title, article_text

    # takes a file reader object and yields
    # lines in it, after tokenisation and punctuation removal,
    # until the line matches the xml closing tag
    def get_text(self, cur_file_iter):
        for line in cur_file_iter:
            line = line.rstrip()
            if line == "":
                continue

            if self.match_xml_closing(line):
                return

            if self.count_elements:
                self.counts["paragraphs"] += 1

            tokenised = self.tok(line)
            clean = self.char_cleaner(tokenised)

            clean = clean.lower() if self.do_lower else clean

            split_words = clean.split()

            if self.count_elements:
                self.counts["words"] += len(split_words)

            yield split_words


if __name__ == '__main__':
    # WikiExtractor call: python WikiExtractor.py -b 5M -o FI FI/fiwiki-latest-pages-articles-multistream.xml

    language = "ALS"
    corpus_dir = "Wikiextractor" + language

    # tokenises around any non-alphanum character
    # (and drops this character)
    alphanum_tok = RegexpTokenizer(r'\w+')

    toktok = ToktokTokenizer()

    special_chars = get_special_char_regexp()


    special_char_remover = lambda s: special_chars.sub(' ', s)

    w = WikiReader(corpus_dir, toktok, special_char_remover)

    wiki_iter = w.article_iter()

    print("Iterator set up...")

    ks, vs = list(zip(*wiki_iter))

    print("Iterator exhausted...")

    print('First (k, v) pair', ks[0], vs[0], len(vs[0]), sep=': ')

    print('Number of articles: ', len(ks))
    print('Number of empty articles:', len(w.empty_articles))

    article_lengths = map(lambda a: len(a), vs)

    length_counts = Counter(article_lengths)

    print('Frequencies of number of paragraphs per arcticle:\n\t', length_counts)

    ls, cs = list(zip(*sorted(length_counts.items(), key= lambda tup: tup[0])))

    plt.semilogx(ls, cs)
    plt.show()
