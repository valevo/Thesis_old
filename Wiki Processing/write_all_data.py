from os import getpid
from psutil import Process
from time import time


from nltk.tokenize import ToktokTokenizer

from CorpusSplitter import ArticleSplitter, ParagraphSplitter, WordSplitter
from special_characters import get_special_char_regexp
from WikiReader import WikiReader
from CorpusCounter import CorpusCounter
from DataWriter import TableWriter, StatsWriter

import matplotlib.pyplot as plt


class TimeAndMemoryTracker:
    def __init__(self, initial_mem=None, initial_time=None):
        if initial_mem is None:
            self.proc = Process(getpid())
            self.mem0 = self.proc.memory_full_info().rss
        else:
            self.mem0 = initial_mem

        if initial_time is None:
            self.t0 = time()
        else:
            self.t0 = initial_time

    def current_relative_info(self, event_name):
        print('\t', event_name, '\t(current memory: ', self.proc.memory_full_info().rss / self.mem0, ')',
              '\t(time elapsed: ', time() - self.t0, ')')

    def update_memory(self, new_mem):
        self.mem0 = new_mem

    def update_time(self, new_time):
        self.t0 = new_time


def zipf_plot(ranks, counts, show_now=True):
    plt.loglog(ranks, counts, '.')
    plt.grid()
    if show_now:
        plt.show()

if __name__ == '__main__':
    corpus_dir = "Wikiextractor/"
    current_tokeniser = ToktokTokenizer

    special_chars = get_special_char_regexp()
    special_char_remover = lambda s: special_chars.sub(' ', s)

    for language in ["EO", "EU", "FI", "ID", "NO", "TR", "VI"]:
        for current_split_lvl in [ArticleSplitter, ParagraphSplitter, WordSplitter]:

            tracker = TimeAndMemoryTracker()
            stats_keeper = StatsWriter()
            print("### Processing ", language, " on splitting level ", current_split_lvl.__name__)


            wiki = WikiReader(corpus_dir + language, tokeniser=current_tokeniser(),
                              char_cleaner=special_char_remover, count_elements=True)
            tracker.current_relative_info('reader set up')

            splitter = current_split_lvl(wiki.article_iter)
            wiki_iter1, wiki_iter2 = splitter.get_iterators()

            tracker.current_relative_info('corpus split')

            wiki_counter1 = CorpusCounter(wiki_iter1)
            tracker.current_relative_info('part 1 counted')

            wiki_counter2 = CorpusCounter(wiki_iter2)
            tracker.current_relative_info('part 2 counted')

            wiki_words, wiki_ranks, wiki_counts = wiki_counter1.align_words_ranks_counts(wiki_counter2)
            tracker.current_relative_info('counts and ranks aligned')

            writer = TableWriter([wiki_words, wiki_ranks, wiki_counts], ["word", "rank", "count"])
            countfile_name = "_".join([language, current_tokeniser.__name__, current_split_lvl.__name__])
            writer.write('Estimates/' + countfile_name)

            print("Relative size of subset 1: ",
                  sum(splitter.generated_flags)/len(splitter.generated_flags))


            print('\tmost common: ', wiki_counter1.most_common(10))
            print('\thighest ranked: ', wiki_counter2.most_common(10))

            zipf_plot(wiki_ranks, wiki_counts)




            words_1 = set(wiki_counter1.keys())
            words_2 = set(wiki_counter2.keys())


            stats_keeper.add_stats("number of types", len(words_1 | words_2))
            stats_keeper.add_stats("relative number of types in subset 1",
                                   len(words_1)/len(words_1 | words_2))
            stats_keeper.add_stats("number of tokens", sum(wiki_counter1.values()) +
                                   sum(wiki_counter2.values()))
            stats_keeper.add_stats("TTR", len(words_1 | words_2) / (sum(wiki_counter1.values()) +
                                                                    sum(wiki_counter2.values())))
            stats_keeper.add_stats("types in intersection", len(words_1 & words_2))
            stats_keeper.add_stats("tokens in intersection",
                                   sum(wiki_counter1[k] + wiki_counter2[k] for k in (words_1 & words_2)))
            reader_stats, reader_vals = list(zip(*wiki.counts.items()))
            stats_keeper.add_stats(reader_stats, reader_vals, multiple=True)

            discordant_pairs = [(tup1, tup2) for tup1, tup2 in
                               zip(wiki_counter1.most_common(), wiki_counter2.most_common())
                                if not tup1[0] == tup2[0]]
            stats_keeper.add_stats("highest ranked discordant pair", discordant_pairs[0])


            print("\n\n")
            stats_keeper.print()
            stats_keeper.pickle("Estimates/Additional Stats/" +
                                language + "_" + current_split_lvl.__name__)


            print("."*200)
        print("#"*200)

