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
        # Overload the cleanup function
        print("completed")

    def mainloop(self):
        # Start the library Call
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
        delta_mem = 0
        max_memory = 0
        memory_usage_refresh = .005
        result = []

        while True:
            time.sleep(memory_usage_refresh)
            current_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            delta_mem = current_mem - start_mem
            if delta_mem > max_memory:
                max_memory = delta_mem
            print("Memory Usage During Call: %d MB" % (delta_mem / 1000))
            if mythread.isShutdown():
                print(mythread.results.time)
                break

        print("MAX Memory Usage in MB: " + str(round(max_memory / 1000.0, 3)))
        result.append((len(self.text),
                       len(self.pattern),
                       round(max_memory / 1000.0, 3)))
        return result


class Tester(unittest.TestCase):
    def test_measure(self):
        text, pattern = Textgen('text.txt').generate(1000000)
        results = Memograph(finder.Hash, text, pattern,
                            finder.Hash.Linear).measure()
        print(f'{results}')
        # results = Memograph(finder.BoyerMoore, text, pattern).measure()
        # print(results)
