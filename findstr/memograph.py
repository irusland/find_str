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
        print("started")

    def cleanup(self):
        print("completed")

    def mainloop(self):
        if self.params is not None:
            self.results = self.algorithm(self.pattern, self.params).search(
                self.text)
        else:
            self.results = self.algorithm(self.pattern).search(self.text)

        self.stop()


class Memograph:
    def __init__(self, algorithm, text, pattern, params=None):
        self.algorithm = algorithm
        self.params = params
        self.text = text
        self.pattern = pattern

    def measure(self):
        if self.params is not None:
            mythread = Runner(self.algorithm,
                              self.text,
                              self.pattern,
                              self.params)
        else:
            mythread = Runner(self.algorithm,
                              self.text,
                              self.pattern)
        mythread.start()

        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mid_memory = 0
        count = 1
        memory_usage_refresh = .005
        result = []

        while True:
            time.sleep(memory_usage_refresh)
            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem

            mid_memory /= count
            mid_memory += delta_mem
            count += 1
            mid_memory *= count

            # print(f'Memory Usage During Call: {delta_mem} B')
            if mythread.isShutdown():
                print(mythread.results.time)
                break

        # print("Memory Usage in Bytes: " + str(round(mid_memory)))
        result.append((len(self.text),
                       len(self.pattern),
                       round(mid_memory)))
        return result


class Tester(unittest.TestCase):
    def test_measure(self):
        text, pattern = Textgen('text.txt').generate(100000, 1000)
        results = Memograph(finder.BruteForce, text, pattern).measure()
        print(f'{results}')
        results = Memograph(finder.Hash, text, pattern,
                            finder.Hash.RabinKarph).measure()
        print(f'{results}')
        results = Memograph(finder.Automate, text, pattern).measure()
        print(f'{results}')
