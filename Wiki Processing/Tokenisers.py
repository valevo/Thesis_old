from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer, ToktokTokenizer, WordPunctTokenizer, PunktSentenceTokenizer

import re

from WikiReader import WikiReader


class Tokeniser:
    def __init__(self):
        self.tok = None

    def tokenise(self, sentence):
        return sentence

    def tokenise_list(self, sentence_list):
        for sentence in sentence_list:
            yield sentence


# for this tokeniser, any alphanumeric
# sequence is a token, any other characters will
# be split around and removed
class AlphaNumTokeniser(Tokeniser):
    def __init__(self):
        super(AlphaNumTokeniser, self).__init__()
        self.tok = RegexpTokenizer(r'\w+')

    def tokenise_list(self, sentence_list):
        for sentence in sentence_list:
            yield self.tok.tokenize(sentence)

    def tokenise(self, sentence):
        return self.tok.tokenize(sentence)


class TokTokTokeniser(Tokeniser):
    def __init__(self):
        super(TokTokTokeniser, self).__init__()
        self.tok = ToktokTokenizer


def head(iterable, size=10):
    return [next(iterable) for _ in range(size)]

if __name__ == '__main__':

    # pipeline:
        # 0. split sentences
        # 1. remove special characters
        # 2. tokenise
        # 3. lemmatise

    language = "VI"
    corpus_dir = "Wikiextractor/" + language

    special_chars = re.compile('[.,:;!?'  # punctuation
                               '\[({})\]'  # parentheses
                               '@#\$&%§+~_"]')  # rest

    char_cleaner = lambda s: special_chars.sub('', s)

    w = WikiReader(corpus_dir)

    w_iter = w.article_iter()

    titles, articles = list(zip(*head(w.article_iter())))

    print(titles)

    print()

    re_tok = RegexpTokenizer(r'\w+')

    toktok = ToktokTokenizer()

    for i in range(5):

        print('\n######################################################################\n')

        first_par = articles[i][0][0]

        print(first_par)

        print()

        print('RE\t\t\t', re_tok.tokenize(first_par))

        print()

        print('TokTok\t\t', toktok.tokenize(first_par))

        print()

        print('clean+TokTok', toktok.tokenize(char_cleaner(first_par)))

        print()

        print('TokTok+clean', list(map(char_cleaner, toktok.tokenize(first_par))))

    print('\n######################################################################\n\n\n')

    wiki_head = head(w.article_iter(), size=1000)

    articles = [a for t, a in wiki_head]

    paragraphs_re = [re_tok.tokenize(text[0]) for paragraph in articles for text in paragraph]

    # print(paragraphs_re[0])

    paragraphs_toktok = [toktok.tokenize(text[0]) for paragraph in articles for text in paragraph]

    paragraphs_toktok_clean = [toktok.tokenize(char_cleaner(text[0]))
                               for paragraph in articles for text in paragraph]

    re_toktok_diff = [len(re_text) - len(toktok_text)
                      for re_text, toktok_text in zip(paragraphs_re, paragraphs_toktok)]


    re_set = set((word for text in paragraphs_re for word in text))

    toktok_set = set((word for text in paragraphs_toktok for word in text))

    print('RE\\TokTok', re_set - toktok_set)

    print('TokTok\\RE', toktok_set - re_set)


    from numpy import mean

    import matplotlib.pyplot as plt

    print('µ(RE-TokTok)', mean(re_toktok_diff))

    plt.plot(list(range(len(re_toktok_diff))), re_toktok_diff, 'x')

    plt.show()


    print('--- clean ---')


    re_toktok_clean_diff = [len(re_text) - len(toktok_text)
                            for re_text, toktok_text in zip(paragraphs_re, paragraphs_toktok_clean)]


    toktok_clean_set = set((word for text in paragraphs_toktok_clean for word in text))

    print(re_set - toktok_clean_set)

    print(toktok_clean_set - re_set)

    print(mean(re_toktok_clean_diff))

    plt.plot(list(range(len(re_toktok_clean_diff))), re_toktok_clean_diff, 'x')

    plt.show()
