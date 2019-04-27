import time as timer

class Chronograph:
    def __init__(self, algorithm, **params):
        self.algorithm = algorithm

    def measure(self):
        text, pattern = Generator.generate(100, 10)
        base_time = self.algorithm(pattern).search(text)
