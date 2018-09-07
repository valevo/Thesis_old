import os
import re

import timeit

from collections import defaultdict

from polyglot.text import Text
from nltk.tokenize import ToktokTokenizer

from special_characters import get_special_char_regexp
from WikiReader import WikiReader

import multiprocessing as mp


class WikiIter:
    @staticmethod
    def get_files(directory):
        # variables for file iteration
        os_walk = list(os.walk(directory))
        if not os_walk:
            raise FileNotFoundError("os.walk(" + directory + ") was empty. Does it exist?")
        all_files = (cur_dir + "/" + f for cur_dir, _, dir_files in os_walk for f in dir_files)
        relevant_name = re.compile("wiki_[0-9]+$")
        return sorted(filter(relevant_name.search, all_files))

    def __init__(self, directory, line_processor, skip_titles=True):
        self.filenames = iter(WikiIter.get_files(directory))
        self.processor = line_processor
        self.skip_titles = skip_titles

        self.cur_file = next(self.filenames)
        self.cur_article_iter = ArticleIter(self.cur_file, self.processor, self.skip_titles)

        self.already_iterated = False

    def __iter__(self):
        if self.already_iterated:
            raise StopIteration("This WikiIter instance has already been exhausted.")
        return self

    def __next__(self):
        try:
            next_article = next(self.cur_article_iter)
            return next_article

        except StopIteration:
            print("FILE DONE", self.cur_file)
            try:
                self.cur_file = next(self.filenames)
                print("FOUND THIS FILE: ", self.cur_file)
                self.cur_article_iter = ArticleIter(self.cur_file, self.processor, self.skip_titles)
                return self.__next__()
            except StopIteration:
                self.already_iterated = True
                print("ALL FILES DONE")
                raise StopIteration

    @classmethod
    def from_file_list(cls, file_list, line_processor, skip_titles=True):
        cls_instance = cls(".", line_processor, skip_titles)
        cls_instance.filenames = iter(file_list)
        return cls_instance


class ArticleIter:
    WikiExtractor_doc_open = re.compile('<doc id="([0-9]+)" url="(.*)" title="(.*)">')
    WikiExtractor_doc_close = re.compile('</doc>')

    @staticmethod
    # matches a given line with the regexp above
    def match_xml_opening(xml_line):
        return ArticleIter.WikiExtractor_doc_open.match(xml_line)

    # matches a given line with the regexp above
    @staticmethod
    def match_xml_closing(xml_line):
        return ArticleIter.WikiExtractor_doc_close.match(xml_line)

    def __init__(self, filename, line_processor, skip_title=False):
        self.file_handle = open(filename, encoding="utf-8")
        self.processor = line_processor
        self.skip_title = skip_title

        self.cur_lineiter = LineIter(self.file_handle, line_processor, stop_signal=self.match_xml_closing)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_line = next(self.file_handle)
            next_line = next_line.rstrip()
            # print(next_line)

            if self.match_xml_opening(next_line): # should always be True
                cur_title = self.match_xml_opening(next_line).groups()[2]
                if self.skip_title:  # advance the file one more line after the open tag to skip title
                    next(self.file_handle)
            else:
                raise ValueError("FOUND THIS LINE : ", next_line)

            article_text = list(self.cur_lineiter)
            self.cur_lineiter = LineIter(self.file_handle, self.processor,
                                         stop_signal=self.match_xml_closing)

            print("done with article: ", cur_title)
            return cur_title, article_text
        except StopIteration:
            print("done with file: ", self.file_handle.name)
            self.file_handle.close()
            raise StopIteration
        # except ValueError:
        #     raise StopIteration


class LineIter:
    def __init__(self, file_handle, line_processor, stop_signal):
        # print("inside init, cur pos in file: ", file_handle.tell())
        self.handle = file_handle
        self.processor = line_processor
        self.stop = stop_signal

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_line = next(self.handle)
            next_line = next_line.rstrip()

            if self.stop(next_line):
                raise StopIteration
            else:
                proc_line = self.processor(next_line)
                return proc_line if proc_line else self.__next__()

        except StopIteration:
            raise StopIteration("THIS SHOULD NOT HAPPEN "
                                "\n\t(FILE ENDED BUT CLOSING TAG NOT FOUND)!")


class PolyGlotTokeniser:
    def __init__(self, language_code=None, char_filter=None):
        self.line_counter = defaultdict(int)
        self.memoizer = dict()
        self.lang = language_code
        self.char_filter = char_filter

    def process_line(self, line):
        if not line:
            return ""
        self.line_counter[line] += 1
        return self.tokens_memoized(line)

    def tokens_memoized(self, line):
        if line in self.memoizer:
            return self.memoizer[line]
        else:
            new_text = Text(line, hint_language_code=self.lang).tokens
            if self.char_filter:
                new_text = list(filter(self.char_filter, new_text))
            self.memoizer[line] = new_text
            return new_text

if __name__ == '__main__':
    pool = mp.Pool()

    wiki_dir = "/home/valentin/Desktop/Wikis"
    cur_lang = "ALS"

    # myiter = WikiIter(wiki_dir + "/" + cur_lang, line_processor=lambda line: len(str.rstrip(line).split()))

    # char_filter = lambda char: char not in {".", ",", '’', ')', '"', '(', '‘'}
    # char_filter = lambda s: not get_special_char_regexp().match(s)
    # proc = PolyGlotTokeniser(language_code="de", char_filter=char_filter)
    #
    # art_iter = ArticleIter("/".join([wiki_dir, cur_lang, "wiki_00"]), proc.process_line, skip_title=True)
    # arts_00 = list(art_iter)
    # print(len(arts_00))
    # print(sorted(proc.line_counter.items(), key=lambda tup: tup[1], reverse=True)[:10])


    line_proc = lambda l: l

    wiki_iter = WikiIter(wiki_dir+"/"+cur_lang, line_processor=line_proc)

    list(wiki_iter)

    print("####"*50 + "\n" + "SECOND ITERATION" + "\n" + "####"*50)
    #
    # list(wiki_iter)
    # #
    # # list(wiki_iter)

