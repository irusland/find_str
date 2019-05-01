import resource
import time
import unittest
import finder
from textgen import *

from stoppable_thread import StoppableThread


class Runner(StoppableThread):
    def __init__(self, algorithm, text, pattern, params=None):
        super(Runner, self).__init__()
        self.algorithm = algorithm
        self.params = params
        self.text = text
        self.pattern = pattern
        self.results = None

    def startup(self):
        pass

    def cleanup(self):
        pass

    def mainloop(self):
        if self.params is not None:
            self.results = self.algorithm(self.pattern, self.params).search(
                self.text)
        else:
            self.results = self.algorithm(self.pattern).search(self.text)

        self.stop()


class Memograph:
    def __init__(self, algorithm, params=None):
        self.algorithm = algorithm
        self.params = params
        # self.text = text
        # self.pattern = pattern

    def measure(self, text, pattern):
        if self.params is not None:
            mythread = Runner(self.algorithm,
                              text,
                              pattern,
                              self.params)
        else:
            mythread = Runner(self.algorithm,
                              text,
                              pattern)
        mythread.start()

        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        max_memory = 0
        memory_usage_refresh = .005

        while True:
            time.sleep(memory_usage_refresh)
            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)\
                        - start_mem

            if delta_mem > max_memory:
                max_memory = delta_mem

            # print(f'Memory Usage During Call: {delta_mem} B')
            if mythread.isShutdown():
                # print(mythread.results.found_indexes)
                break

        # print("Memory Usage in Bytes: " + str(max_memory))
        return round(max_memory / 2**20)


class Tester(unittest.TestCase):
    def test_measure(self):
        text, pattern = Textgen('text.txt').generate(1000, 100)
        results = Memograph(finder.BruteForce).measure(text, pattern)
        print(f'{results}')
        results = Memograph(finder.Hash, finder.Hash.RabinKarph).measure(text, pattern)
        print(f'{results}')
        results = Memograph(finder.KMP).measure(text, pattern)
        print(f'{results}')
