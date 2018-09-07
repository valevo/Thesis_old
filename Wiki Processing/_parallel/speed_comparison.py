import timeit
import time
from tqdm import tqdm


import multiprocessing as mp
from _parallel.iter_test import WikiIter, ArticleIter
from polyglot.text import Text

def identity(line):
    return line


def pos_tag(line):
    line = line.rstrip()
    if line == "":
        return ""
    return Text(line, hint_language_code="eo").transfer_pos_tags


def get_file_content(file):
    return list(ArticleIter(file, pos_tag))

if __name__ == '__main__':
    # WikiReader with ToktokTokeniser
    # 110.67141040699971
    # print(timeit.timeit(stmt="list(wiki_reader.article_iter())",
    #                     setup="wiki_dir = '/home/valentin/Desktop/Wikis';"
    #                           "cur_lang = 'ALS';"
    #                           "from nltk.tokenize import ToktokTokenizer;"
    #                           "from special_characters import get_special_char_regexp;"
    #                           "from WikiReader import WikiReader;"
    #                           "wiki_reader = WikiReader(wiki_dir+'/'+cur_lang, ToktokTokenizer(), lambda s: get_special_char_regexp().sub('', s));",
    #                     number=3))


    # # WikiIter with polyglot.Text tokeniser
    # print(timeit.timeit(stmt="list(wiki_iter)",
    #                     setup="wiki_dir = '/home/valentin/Desktop/Wikis';"
    #                           "cur_lang = 'Test';"
    #                           "from special_characters import get_special_char_regexp;"
    #                           "from _parallel.iter_test import PolyGlotTokeniser, WikiIter;"
    #                           "char_filter = lambda s: not get_special_char_regexp().match(s);"
    #                           "proc = PolyGlotTokeniser(language_code='de', char_filter=char_filter);"
    #                           "wiki_iter = WikiIter(wiki_dir+'/'+cur_lang, line_processor=proc.process_line);",
    #                     number=3))

    # WikiIter with ToktokTokeniser
    # 157.354277
    # print(timeit.timeit(stmt="wiki_iter = WikiIter(wiki_dir+'/'+cur_lang, proc);"
    #                          "list(wiki_iter)",
    #                     setup="wiki_dir = '/home/valentin/Desktop/Wikis';"
    #                           "cur_lang = 'ALS';"
    #                           "from special_characters import get_special_char_regexp;"
    #                           "from nltk.tokenize import ToktokTokenizer;"
    #                           "from _parallel.iter_test import PolyGlotTokeniser, WikiIter;"
    #                           "toktok = ToktokTokenizer();"
    #                           "char_regexp = get_special_char_regexp();"

    #                           "char_filter = lambda s: not char_regexp.match(s);"
    #                           "proc = lambda l: list(filter(char_filter, toktok.tokenize(l)));",
    #                     number=3))

    pool = mp.Pool()

    # files = ['/home/valentin/Desktop/Wikis/ALS/wiki_00',
    #          '/home/valentin/Desktop/Wikis/ALS/wiki_01',
    #          '/home/valentin/Desktop/Wikis/ALS/wiki_02',
    #          '/home/valentin/Desktop/Wikis/ALS/wiki_03']

    wiki_dir = "/home/valentin/Desktop/Wikis"
    cur_lang = "EO"

    files = WikiIter.get_files(wiki_dir+'/'+cur_lang)

    # file_contents = pool.map(get_file_content, files)
    #
    #


    # t0 = time.time()
    #
    # art_iter = ArticleIter(files[0], identity)
    #
    # first = next(art_iter)[1]
    #
    # first_str = "\n".join(first)
    #
    # print(Text(first_str, hint_language_code="eo").transfer_pos_tags)
    #
    # print("TIME: ", time.time() - t0)
    #


    tag_times = []

    t0 = time.time()

    art_iter = ArticleIter(files[0], pos_tag)

    # t1 = time.time()
    #
    # arts_pos = list(map(lambda art:
    #                     [Text(s, hint_language_code="eo").transfer_pos_tags for s in art[1]],
    #                     art_iter))
    #
    for i, (title, art) in enumerate(art_iter):
        # t1 = time.time()
        # # tags = [Text(s.rstrip(), hint_language_code="eo").transfer_pos_tags for s in art]
        # cur_t = time.time() - t1
        # print("TIME pos tagging: ", cur_t)
        # tag_times.append(cur_t)
        tags = art

        if i > 150:
            break

    print("TIME: ", time.time() - t0)
    # print("AVG TAG TIME: ", sum(tag_times)/len(tag_times))



# TIME:  53.53782629966736
# AVG TAG TIME:  0.35187944456150655