from nltk.tokenize import ToktokTokenizer, RegexpTokenizer
from WikiReader import WikiReader
import re

from collections import Counter

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # read the Wiki
    language = "FI"
    corpus_dir = "Wikiextractor/" + language

    re_tok = RegexpTokenizer(r'\w+')

    toktok_tok = ToktokTokenizer()

    special_chars = re.compile('[.,:;!?'  # punctuation
                               '\[({})\]\"\''  # parentheses
                               '@#\$&%§+~_]')  # rest

    special_char_remover = lambda s: special_chars.sub('', s)

    w = WikiReader(corpus_dir, toktok_tok, special_char_remover)

    wiki_iter_func = w.article_iter

    #################################
    # inspect first article
    first_title, first_t = next(wiki_iter_func())

    print(first_title)
    print(first_t)
    print(len(first_t))
    print([len(par) for par in first_t])

    print('\n\n\n')


    # calling zip(*wiki_iter) is not okay (takes too long)
    texts_tok = list((art for title, art in wiki_iter_func()))

    print('Zipped...')

    #################################
    # basic stats
    print('Number of articles: ', len(texts_tok))
    print('Number of empty articles:', len(w.empty_articles))

    #################################
    # stats on paragraphs
    article_lengths = map(lambda a: len(a), texts_tok)

    length_counts = Counter(article_lengths)

    print('Frequencies of number of paragraphs per article:\n\t', length_counts.most_common(100))

    lengths, counts = list(zip(*sorted(length_counts.items())))

    plt.semilogx(lengths, counts)
    plt.title('Number of articles in terms of number of paragraphs')
    plt.show()



    print('\n\n\n')

    #################################
    # stats on words
    text_tok_lengths = map(lambda t: sum(len(par) for par in t), texts_tok)

    print('Length summed...')

    text_length_counts = Counter(text_tok_lengths)

    print('Tokenised text length counts:\n\t', text_length_counts)

    lengths, counts = list(zip(*sorted(text_length_counts.items())))

    plt.semilogx(lengths, counts, '.')

    plt.title('Number of articles in terms of number of words')


    plt.show()

    plt.xscale('log')

    plt.hist(list((sum(len(par) for par in t) for t in texts_tok)), bins=100)

    plt.title('Number of articles in terms of number of words')

    plt.show()
