import time as timer
import unittest
import finder


class Chronograph:
    def __init__(self, algorithm, param=None, generator=None):
        self.algorithm = algorithm
        self.param = param
        self.generator = generator

    def open_file(self):
        with open('text.txt') as t:
            yield t.read()
        with open('pattern.txt') as p:
            yield p.read()

    def measure(self, text, pattern):
        start = timer.time()
        if self.param is not None:
            result = self.algorithm(pattern, self.param).search(text)
        else:
            result = self.algorithm(pattern).search(text)
        stop = timer.time()
        assert result is not None, 'Result is None'
        return stop - start

    def get_repetitions(self, time):
        return round(1 / time)

    def measure_accurate(self, t, p):
        time = self.measure(t, p)
        cycles = self.get_repetitions(time)
        for i in range(cycles):
            time += self.measure(t, p)
        if cycles != 0:
            return time / cycles
        return time

    def measure_generator(self, generator):
        pass

class ChronoTester(unittest.TestCase):
    def test_open(self):
        c = Chronograph('')
        t, p = c.open_file()
        self.assertTrue(len(p) == 5)
        self.assertTrue(len(t) > 100)

    def test_measure(self):
        c = Chronograph(finder.Hash, finder.Hash.Linear)
        t, p = c.open_file()
        time = c.measure(t, p)
        self.assertTrue(time != 0)

    def test_measure_accurate_small(self):
        c = Chronograph(finder.Hash, finder.Hash.Linear)
        t, p = 'aaabbbaba', 'ab'
        times = []
        for i in range(10):
            times.append(c.measure_accurate(t, p))
        base_time = times[0]
        count = 1
        for time in times:
            self.assertAlmostEqual(time, base_time, delta=1e-5)
            base_time *= count
            base_time += time
            count += 1
            base_time /= count

    def test_measure_accurate_big(self):
        c = Chronograph(finder.Hash, finder.Hash.Linear)
        t, p = c.open_file()
        times = []
        for i in range(3):
            times.append(c.measure_accurate(t, p))
        base_time = times[0]
        count = 1
        for time in times:
            self.assertAlmostEqual(time, base_time, delta=1e-1)
            base_time *= count
            base_time += time
            count += 1
            base_time /= count
