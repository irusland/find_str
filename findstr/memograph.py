import finder
from textgen import Textgen
from memory_profiler import memory_usage


class Memograph:
    def __init__(self, algorithm, params=None):
        self.algorithm = algorithm
        self.params = params

    def run(self, text, pattern):
        if self.params is not None:
            return self.algorithm(pattern, self.params).search(text)
        else:
            return self.algorithm(pattern).search(text)

    def measure(self, text, pattern):
        mem = memory_usage(proc=(self.run, (text, pattern)), max_usage=True)[0]

        return mem


class Measurer:
    def measure(self):
        text, pattern = Textgen('text.txt').generate(1000000, 1000)
        print(f'{Memograph(finder.BruteForce).measure(text, pattern)}')
        print(f'{Memograph(finder.Hash,finder.RabinKarph).measure(text, pattern)}')
        print(f'{Memograph(finder.KMP).measure(text, pattern)}')


if __name__ == '__main__':
    Measurer.measure(Measurer())
