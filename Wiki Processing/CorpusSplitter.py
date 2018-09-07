from numpy import random


# IMPORTANT: this class assumes that the iterator 'reader_func'
# always has the same elements and order of iteration
class CorpusSplitter:
    def __init__(self, corpus_reader_func, prob=0.5, given_flags=None):
        self.iter_func = corpus_reader_func
        self.iter1 = corpus_reader_func()
        self.iter2 = corpus_reader_func()

        self.p = prob
        if given_flags:
            self.flag_iter = given_flags
        else:
            self.flag_iter = self.random_flags()
        self.generated_flags = []

    def random_flags(self):
        while True:
            yield 1 if random.random() >= self.p else 0

    def rand_filter(self, iterable, negate):
        for i, elem in enumerate(iterable):
            cur_flag = self.get_next_flag(i)
            if negate:
                if not cur_flag:
                    yield elem
            else:
                if cur_flag:
                    yield elem

    def get_next_flag(self, i):
        if i >= len(self.generated_flags):
            cur_flag = next(self.flag_iter)
            self.generated_flags.append(cur_flag)
            return cur_flag
        else:
            return self.generated_flags[i]

    def get_iterators(self):
        pass


class ArticleSplitter(CorpusSplitter):
    def __init__(self, wiki_reader_func, prob=0.5, given_flags=None):
        super(ArticleSplitter, self).__init__(wiki_reader_func, prob, given_flags)

    def get_iterators(self):
        return self.rand_filter(self.article_iter(self.iter1), negate=False), \
               self.rand_filter(self.article_iter(self.iter2), negate=True)

    @staticmethod
    def article_iter(wiki_reader):
        for title, article in wiki_reader:
            yield article


class ParagraphSplitter(CorpusSplitter):
    def __init__(self, wiki_reader_func, prob=0.5, given_flags=None):
        super(ParagraphSplitter, self).__init__(wiki_reader_func, prob, given_flags)

    def get_iterators(self):
        return self.rand_filter(self.paragraph_iter(self.iter1), negate=False), \
               self.rand_filter(self.paragraph_iter(self.iter2), negate=True)

    @staticmethod
    def paragraph_iter(wiki_reader):
        for title, article in wiki_reader:
            for paragraph in article:
                yield paragraph


class WordSplitter(CorpusSplitter):
    def __init__(self, wiki_reader_func, prob=0.5, given_flags=None):
        super(WordSplitter, self).__init__(wiki_reader_func, prob, given_flags)

    def get_iterators(self):
        return self.rand_filter(self.word_iter(self.iter1), negate=False), \
               self.rand_filter(self.word_iter(self.iter2), negate=True)

    @staticmethod
    def word_iter(wiki_reader):
        for title, article in wiki_reader:
            for paragraph in article:
                for word in paragraph:
                    yield word