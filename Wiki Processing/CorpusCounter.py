from collections import Counter


class CorpusCounter(Counter):
    def __init__(self, corpus_iter, atom_type=str):
        first = next(corpus_iter)
        self.original_it = self.append_iterable(first, corpus_iter)

        try:
            if isinstance(first, atom_type):
                self.it = self.original_it
            elif isinstance(first[0], atom_type):
                self.it = self.words_from_pars()
            elif isinstance(first[0][0], atom_type):
                self.it = self.words_from_articles()
            else:
                raise ValueError("Depth of nesting not supported")
        except TypeError:
            print('subscripting failed with: ', first)

        super(CorpusCounter, self).__init__(self.it)

    def words_from_pars(self):
        for par in self.original_it:
            for w in par:
                yield w

    def words_from_articles(self):
        for art in self.original_it:
            for par in art:
                for w in par:
                    yield w

    def align_ranks_counts(self, other=None, separate=True):
        count_dict = self if other is None else other
        rank_count_iter = ((r, count_dict[w]) for w, r in self.rank_iter())

        if separate:
            return zip(*rank_count_iter)
        else:
            return rank_count_iter


    # aligns words, ranks and counts of the corpus, sorted by ranks
    # IF other is not None THEN
    #   the ranks of this counter are paired with the counters of the other counter
    def align_words_ranks_counts(self, other=None, separate=True):
        count_dict = self if other is None else other

        word_rank_count_iter = ((w, r, count_dict[w]) for w, r in self.rank_iter())

        if separate:
            return zip(*word_rank_count_iter)
        else:
            return word_rank_count_iter

    def rank_iter(self):
        for i, (w, c) in enumerate(self.most_common(), start=1):
            yield w, i

    @staticmethod
    def append_iterable(x, iterable):
        # print('X', x)
        yield x
        for y in iterable:
            # print("Y", y)
            yield y

    # # same as itertools.chain([elem], iterator)
    # @staticmethod
    # def append_iterable(iter1, iter2):
    #     try:
    #         for x in iter1:
    #             print(x)
    #             yield x
    #     except TypeError:
    #         yield iter1
    #     try:
    #         for x in iter2:
    #             yield x
    #     except TypeError:
    #         yield iter2