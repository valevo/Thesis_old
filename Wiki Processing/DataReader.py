# -*- coding: utf-8 -*-
import os

from collections import Counter

from polyglot.text import Word, Text

from DataWriter import TableWriter


class DataReader:
    def __init__(self, file_name):
        self.file = open(file_name, mode="r", encoding="utf-8")

    def read_data(self):
        return list(self.line_iter())

    def line_iter(self):
        for line in self.file:
            yield line


class TableReader(DataReader):
    def __init__(self, file_name, types, sep="\t", has_header=True):
        super(TableReader, self).__init__(file_name)
        self.sep = sep
        self.has_header = has_header
        self.col_names = None
        self.types = types

    def read_data(self):
        if self.has_header:
            self.col_names = self.file.readline().rstrip().split(self.sep)

        cols = zip(*self.line_iter())

        return Table(cols, names=self.col_names)

    def line_iter(self):
        for line in self.file:
            col_vals = line.rstrip().split(self.sep)
            try:
                yield [t(v) for t, v in zip(self.types, col_vals)]
            except (TypeError, ValueError) as e:
                print("ERROR: type conversion failed for line with values: ",
                      col_vals, "\t types:", self.types)


def head(iterable, l=10):
    return [next(iterable) for i in range(l)]



class Table:
    def __init__(self, cols, names=None):
        # if any(map(lambda c: len(c) != len(cols[0]), cols)):
        #     raise ValueError("Not all columns same lengths!")

        cols = list(cols)

        if names is None:
            self.names = list(range(len(cols)))
        else:
            self.names = names

        self.table = {n: c for n, c in zip(self.names, cols)}
        self.nrows = len(self.table[self.names[0]])

    def __getitem__(self, name):
        if name not in self.names:
            raise ValueError("Column with name ", name, "not in the table")

        return self.table[name]

    def get_names(self):
        return self.names
    def get_cols(self, cols=None):
        if cols is None:
            cols = self.names
        return [self.table[n] for n in cols]

    def add_col(self, col, name=None):
        if name is None:
            name = len(self.names)

        self.names.append(name)
        self.table[name] = col

    def add_row(self, new_row, index=-1):
        if index == -1:
            for col_n, new_val in zip(self.names, new_row):
                self.table[col_n].append(new_val)
        else:
            for col_n, new_val in zip(self.names, new_row):
                cur_col = self.table[col_n]
                self.table[col_n] = cur_col[:index] + [new_val] + cur_col[index+1:]

    def head(self, l=10, include_header=True, for_printing=False):
        if self.nrows <= l:
            l = self.nrows

        if include_header:
            if for_printing:
                names = map(str, self.names)
                yield "\t".join(names)
            else:
                yield self.names

        for i in range(l):
            row = [self.table[n][i] for n in self.names]
            if for_printing:
                row = map(str, row)
                yield "\t\t".join(row)
            else:
                yield row

    def sums(self, cols=None):
        if cols is None:
            cols = self.names
        return [sum(self[c]) for c in cols]


if __name__ == '__main__':
    estimate_dir = "/home/valentin/Desktop/Thesis II/Zipf Error/Estimates"
    lang = "NO"
    estimate_file = lang+"_ToktokTokenizer_ArticleSplitter"

    reader = TableReader(estimate_dir+"/"+estimate_file, [str, int, int])
    table = reader.read_data()


    for row in table.head(for_printing=True):
        print(row)
    print('__'*10)

    print(table.nrows)
    print()
    print(table.sums(cols=["count"]))
    print()


    # print("start tagging")
    #
    # tagged_words = list(map(lambda w: Text(w, hint_language_code=lang).transfer_pos_tags[0],
    #                         table["word"]))
    #
    # print("tagging finished")
    #
    # print(tagged_words[:30])
    #
    #
    # _, tags = list(zip(*tagged_words))
    #
    # tag_counts = Counter(tags)
    # print(tag_counts)

    # import matplotlib.pyplot as plt
    #
    # tags_numerical = []
    #
    # plt.plot(*list(zip(*tag_counts.items())))
    #
    # plt.show()

    import pickle

    # with open(lang+"_tagged_words", "wb") as handle:
    #     pickle.dump(tagged_words, handle)

    tagged_words = pickle.load(open("NO_tagged_words", "rb"))

    _, tags = list(zip(*tagged_words))

    print(tagged_words[:10])

    table.add_col(tags, name="tag")

    for row in table.head(for_printing=True):
        print(row)


    cols = table.get_cols()

    ns = table.get_names()

    print(ns)

    print(head(zip(*cols)))


    writer = TableWriter(cols, ns)

    writer.write(estimate_file + "_POStagged")