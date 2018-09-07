# -*- coding: utf-8 -*-
from os import getpid
from psutil import Process
from time import time

from collections import Counter
import pickle

from nltk.tokenize import RegexpTokenizer, ToktokTokenizer
import matplotlib.pyplot as plt


from WikiReader import WikiReader
from CorpusSplitter import ArticleSplitter, ParagraphSplitter, WordSplitter
from CorpusCounter import CorpusCounter
from special_characters import *


class DataWriter:
    def __init__(self, data, names=None, verbose=True):
        self.data = data
        self.verbose = verbose
        self.names = names


# parameters:
# - tokenisation method
# - special characters removed
# - level of randomly splitting corpus elements (articles, paragraphs, (sentences), words)
# - binary probability of corpus element being used for rank or frequency estimation
# - which of the two created subcorpora is used for rank estimation and which for frequency estimation

# info:
# - language (use Wikipedia code)
# - level of splitting (article, paragraph, ...)
# - number of tokens, types, articles, paragraphs in whole corpus -> types and tokens can be calculated from data itself
# - number of tokens, types, articles, paragraphs in each subcorpus
# - number of types and tokens not in the extracted data set (i.e. the
#       (because the counts were 0 in the subcorpus from which the ranks were estimated)


# written to be read by R's read.table
class TableWriter(DataWriter):
    # data is list of lists
    # names is a list of strings the length of data
    def __init__(self, data, names=None, sep="\t", verbose=True):
        super(TableWriter, self).__init__(data, names, verbose)
        self.data = zip(*self.data)
        self.sep = sep

    def write(self, filename):
        with open(filename, 'w') as handle:
            if self.names:
                handle.write(self.sep.join(self.names))
                handle.write("\n")

            for tup in self.data:
                line = self.sep.join((str(elem) for elem in tup))
                handle.write(line)
                handle.write("\n")

    # prints info to stdout
    def print_info(self):
        pass

    # writes info to the first line of the file
    def write_info(self):
        pass


# generic writer for stats:
# takes names-values pairs and writes
# them in JSON format to std.out or a file or pickles them
class StatsWriter(DataWriter):
    def __init__(self, data=None, names=None):
        if data is None and names is None:
            super(StatsWriter, self).__init__(data=[], names=[])
        elif not(data is None or names is None):
            if not len(data) == len(names):
                raise ValueError("data and names not the same length")
            super(StatsWriter, self).__init__(data=data, names=data)
        else:
            raise ValueError("args data and names have to "
                             "be either both None or both have a value")

    def add_stats(self, new_names, new_values, multiple=False):
        if multiple:
            self.names.extend(new_names)
            self.data.extend(new_values)
        else:
            self.names.append(new_names)
            self.data.append(new_values)

    def sort_by_names(self):
        sorted_n_v_pairs = sorted(zip(self.names, self.data), key=lambda tup: tup[0])
        self.names, self.data = list(zip(*sorted_n_v_pairs))

    def write(self, filename, sort_by_names=False):
        if sort_by_names:
            self.sort_by_names()

        with open(filename, 'w') as handle:
            for n, v in zip(self.names, self.data):
                handle.write(n)
                handle.write(": ")
                handle.write(str(v))
                handle.write(",\n")

    def print(self, sort_by_names=False):
        if sort_by_names:
            self.sort_by_names()

        print("STATS:\n{")

        for n, v in zip(self.names, self.data):
            print(n, end="")
            print(": ", end="")
            print(str(v), end="")
            print(",")
        print("}\n")

    def pickle(self, filename):
        data_dict = dict(zip(self.names, self.data))
        with open(filename, "wb") as handle:
            pickle.dump(data_dict, handle)








if __name__ == '__main__':
    proc = Process(getpid())
    mem0 = proc.memory_full_info().rss
    t0 = time()


    # parameters
    current_split_lvl = ArticleSplitter
    current_tokeniser = ToktokTokenizer
    language = "ALS"
    print("Processing ", language, " on splitting level ", current_split_lvl.__name__)

    #alphanum_tok = RegexpTokenizer(r'\w+')
    special_chars = get_special_char_regexp()
    special_char_remover = lambda s: special_chars.sub(' ', s)



    corpus_dir = "Wikiextractor/" + language
    wiki = WikiReader(corpus_dir, tokeniser=current_tokeniser(), char_cleaner=special_char_remover)

    print('reader set up')

    splitter = current_split_lvl(wiki.article_iter)

    wiki_iter1, wiki_iter2 = splitter.get_iterators()

    print('corpus split', '\t(current memory: ', proc.memory_full_info().rss/mem0, ')',
          '\t(time elapsed: ', time() - t0, ')')

    wiki_counter1 = CorpusCounter(wiki_iter1)

    print('part 1 counted', '\t(current memory: ', proc.memory_full_info().rss/mem0, ')',
          '\t(time elapsed: ', time() - t0, ')\n')

    wiki_counter2 = CorpusCounter(wiki_iter2)

    print('part 2 counted', '\t(current memory: ', proc.memory_full_info().rss/mem0, ')',
          '\t(time elapsed: ', time() - t0, ')\n')

    wiki_words, wiki_ranks, wiki_counts = wiki_counter1.align_words_ranks_counts(wiki_counter2)

    print('counts and ranks aligned', '\t(current memory: ', proc.memory_full_info().rss/mem0, ')',
          '\t(time elapsed: ', time() - t0, ')\n')

    plt.loglog(wiki_ranks, wiki_counts, '.')

    plt.grid()

    plt.show()


    print('most common: ', wiki_counter1.most_common(10))

    print('highest ranked: ', wiki_counter2.most_common(10))

    words_1 = set(wiki_counter1.keys())

    words_2 = set(wiki_counter2.keys())

    print('\nnumber of types (part1, part2) ', len(words_1), len(words_2))

    # union
    print('size of union of types ', len(words_1 | words_2))

    # elements of words_2 that are not in words_1, i.e.
    # words not included in the data set
    print('size of types in part2 but not in part1\n\t', len(words_2 - words_1))

    # symmetric set difference
    print('symmetric diff part1 and part2 ', len(words_1 ^ words_2))

    writer = TableWriter([wiki_words, wiki_ranks, wiki_counts], ["word", "rank", "count"])

    countfile_name = "_".join([language, current_tokeniser.__name__, current_split_lvl.__name__])

    #writer.write('Estimates/' + countfile_name)








