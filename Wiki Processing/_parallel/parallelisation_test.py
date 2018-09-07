import multiprocessing as mp
import os
import re

from WikiReader import WikiReader
from special_characters import get_special_char_regexp

from nltk.tokenize import ToktokTokenizer
from polyglot.text import Text


pool = mp.Pool(processes=4)

def get_filenames(directory):
    os_walk = list(os.walk(directory))
    if not os_walk:
        raise FileNotFoundError("os.walk(" + directory + ") was empty. Does it exist?")
    all_files = (cur_dir + "/" + f for cur_dir, _, dir_files in os_walk for f in dir_files)
    relevant_name = re.compile("wiki_[0-9]+$")
    return sorted(filter(relevant_name.search, all_files))


class WikiReader_from_filelist(WikiReader):

    def __init__(self, directory, tokeniser=None, char_cleaner=None, do_lower=True, count_elements=False):
        super(WikiReader_from_filelist, self).__init__(directory,
                                                       tokeniser, char_cleaner, do_lower, count_elements)

    def article_iter_from_list(self, file_name_list):
        for file in file_name_list:
            print('Opening ', file)
            cur_file_iter = self.get_file_iter(file)
            yield from self.single_file_iter(cur_file_iter)
            # iterated over the Wiki once, don't count in the next iterations
        self.count_elements = False


if __name__ == '__main__':
    wiki_dir = "/home/valentin/Desktop/Wikis"
    cur_lang = "FI"

    toktok = ToktokTokenizer()
    special_chars = get_special_char_regexp()
    special_char_remover = lambda s: special_chars.sub(' ', s)

    reader = WikiReader_from_filelist(wiki_dir+"/"+cur_lang,
                                      tokeniser=toktok, char_cleaner=special_char_remover)

    wiki_iter = reader.article_iter()

    get_articles = lambda it: list(it)

    results = pool.map(reader.single_file_iter, reader.filenames)