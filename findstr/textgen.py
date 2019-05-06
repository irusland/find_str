import random
import finder


class Textgen:
    def __init__(self, *sources):
        if len(sources) == 0:
            raise ValueError('Source not found')
        self.text_sources = sources

    n = 10000
    
    worst_cases = {
        finder.BruteForce: (f'{"aba" * n}abc', 'abc'),
        finder.Linear: (f'{"Zhd" * n}abc', 'abc'),
        finder.Quad: (f'{"cba" * n}abc', 'abc'),
        finder.RabinKarph: (f'{"aca" * n}abc', 'abc'),
        finder.Automate: (f'{"abb" * n}abc', 'abc'),
        finder.BoyerMoore: (f'{"ABCDAB ABCDABCDAB" * n}D', 'ABCDABD'),
        finder.KMP: (f'{"ABC ABCDAB ABCDABCDAB" * n}D', 'ABCDABD'),
        finder.SuffixArray: (f'{"a" * (n // 2)}{"b" * (n // 2)}', 'b'),
    }

    best_cases = {
        finder.BruteForce: (f'abc{"ddd" * n}', 'abc'),
        finder.Linear: (f'{"ddd" * n}abc', 'abc'),
        finder.Quad: (f'{"ddd" * n}abc', 'abc'),
        finder.RabinKarph: (f'{"ddd" * n}abc', 'abc'),
        finder.Automate: (f'{"ccc" * n}abc', 'abc'),
        finder.BoyerMoore: (f'{"D" * n}D', 'ABCDABD'),
        finder.KMP: (f'{"D" * n}D', 'ABCDABD'),
        finder.SuffixArray: (f'abc{"a" * (n // 2)}', 'abc'),
    }

    def generate_for(self, algorithm, best=True):
        if best:
            return self.best_cases[algorithm]
        return self.worst_cases[algorithm]

    def generate(self, text_size, pattern_size=0):
        if text_size < pattern_size:
            raise IndexError
        is_word = pattern_size == 0
        rnd_text = ''
        while len(rnd_text) < text_size:
            pos = random.randint(0, len(self.text_sources) - 1)
            with open(self.text_sources[pos]) as t:
                text = t.read()
            a = random.randint(0, len(text))
            b = random.randint(0, len(text))
            rnd_text += text[min(a, b):max(a, b)]
        rnd_text = rnd_text[:text_size]
        yield rnd_text
        part = ''
        while len(part) < pattern_size:
            char = chr(random.randint(0, 255))
            split = rnd_text.split(char)
            part = split[random.randint(0, len(split) - 1)]

        if is_word:
            split = rnd_text.split(' ')
            pattern = split[random.randint(0, len(split) - 1)]
            while len(pattern) == 0:
                pattern = split[random.randint(0, len(split) - 1)]
            yield pattern
        else:
            i = random.randint(0, len(part))
            if i + pattern_size > len(part):
                yield part[len(part) - pattern_size:]
            else:
                yield part[i:i + pattern_size]
