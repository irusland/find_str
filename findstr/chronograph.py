import time as timer


class Chronograph:
    def __init__(self, algorithm, param=None, generator=None):
        self.algorithm = algorithm
        self.param = param
        self.generator = generator

    @staticmethod
    def open_file():
        with open('text.txt') as t:
            yield t.read()
        with open('pattern.txt') as p:
            yield p.read()

    def measure(self, text, pattern):
        start = timer.perf_counter()
        if self.param is not None:
            result = self.algorithm(pattern, self.param).search(text)
        else:
            result = self.algorithm(pattern).search(text)
        stop = timer.perf_counter()
        assert result is not None, 'Result is None'
        return stop - start

    @staticmethod
    def get_repetitions(time):
        return round(1 / time)

    def measure_accurate(self, t, p):
        time = self.measure(t, p)
        cycles = self.get_repetitions(time)
        for i in range(cycles):
            time += self.measure(t, p)
        if cycles != 0:
            return time / cycles
        return time

    def measure_text_parts(self, text, pattern, part_count):
        part_len = round(len(text) / part_count)
        length = part_len
        result = []
        while length < len(text):
            text_to_search = text[:length]
            length += part_len
            if len(text) - (length - part_len) < part_len:
                text_to_search = text
            time = self.measure_accurate(text_to_search, pattern)
            result.append((length, len(pattern), time))
        return result
