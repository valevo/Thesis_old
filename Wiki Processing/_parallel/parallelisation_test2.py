import multiprocessing as mp

import pickle

class Whatevs:
    def __init__(self, pow):
        self.pow = pow

    def func(self, x):
        return x**self.pow

    def pow_range_gen(self, start):
        for x in range(start, start**self.pow):
            yield x

    def pow_range_iter(self, start):
        return PowRangeIter(start, start**self.pow)


class PowRangeIter:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.cur = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur >= self.end:
            raise StopIteration
        self.cur += 1
        return self.cur - 1



if __name__ == '__main__':
    pool = mp.Pool(processes=4)

    w = Whatevs(2)

    iters = pool.map(w.pow_range_iter, range(10))

    print(iters)

    print(pool.map(list, iters))