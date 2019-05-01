import grapher
from chronograph import Chronograph as Chrono
from memograph import Memograph as Memo
import memograph
import finder
from textgen import Textgen
import numpy


def get_time(points):
    res = []
    for t in points:
        for _, _, time in t:
            res.append(time)
    return min(res), float(numpy.median(res)), max(res)


def main():
    grapher.build_graph()

    sizes = [
        (100000, 0),
        (100, 10),
        (1000, 100),
        (10000, 1000),
        (100000, 100),
        (1000000, 100),
    ]

    for text_size, pattern_size in sizes:
        text, pattern = Textgen('text.txt').generate(text_size)
        print(f'Generated: Text Length = {text_size}, Pattern Size = {pattern_size}')
        results = [
            ('Brute Force',
             Chrono(finder.BruteForce).measure_accurate(text, pattern),
             Memo(finder.BruteForce).measure(text, pattern)),
            ('Hash Linear',
             Chrono(finder.Hash, finder.Hash.Linear).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Hash.Linear).measure(text, pattern)),
            ('Hash Quad',
             Chrono(finder.Hash, finder.Hash.Quad).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Hash.Quad).measure(text, pattern)),
            ('Hash RK',
             Chrono(finder.Hash, finder.Hash.RabinKarph).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Hash.RabinKarph).measure(text, pattern)),
            ('Automate',
             Chrono(finder.Automate).measure_accurate(text, pattern),
             Memo(finder.Automate).measure(text, pattern)),
            ('Boyer Moore',
             Chrono(finder.BoyerMoore).measure_accurate(text, pattern),
             Memo(finder.BoyerMoore).measure(text, pattern)),
            ('KMP',
             Chrono(finder.KMP).measure_accurate(text, pattern),
             Memo(finder.KMP).measure(text, pattern)),
        ]
        results = sorted(results, key=lambda _: _[1])
        for name, time, memory in results:
            print(f'{name}\n\t%.6f S \n\t{memory} MB\n' % time)


if __name__ == '__main__':
    main()