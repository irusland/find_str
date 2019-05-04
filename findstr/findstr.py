import grapher
from chronograph import Chronograph as Chrono
from memograph import Memograph as Memo
import finder
from textgen import Textgen
import statistics


def get_time(points):
    res = []
    for t in points:
        for _, _, time in t:
            res.append(time)
    return min(res), float(statistics.median(res)), max(res)


def main():
    goal = 'This different substring search algorithms testing' \
           'shows dependencies of a string preprocessing and other ' \
           'methods of search optimizing'

    specs = 'Processor: 3.4GHz Inter Core i5 \n' \
            'Memory: 8 GB 1600 MHz DDR3 \n' \
            'System: osx'

    alg_doc = 'Documentation of following algorithms:'

    results_explanation = 'Explanation:\n' \
                          '* Brute Force is pretty stable alghorithm, ' \
                          'works every time with O(n^2) asymptotic\n' \
                          '* Hashes have a collision aspect that\'s why we ' \
                          'can see an abrupt behavior change and time growth' \
                          'on a bad substring\n' \
                          '* Automate has a preprocessing aspect that\'s ' \
                          'why we can see time growth\n' \
                          '* Boyer Moore algorithm works perfectly with ' \
                          'prepared pattern on every text but as we can see ' \
                          'there is recounting shift tables time delay\n' \
                          '* KMP works fine on average string its pretty ' \
                          'stable\n' \
                          '* Suffix Array has a text preprocessing that ' \
                          'allows to work fast with O(n*log(n)) asymptotic ' \
                          'on every pattern\n'

    summary = 'Summary:'

    print(goal)
    print(specs)
    print()
    print(alg_doc)
    print(finder.BruteForce.__doc__)
    print(finder.Hash.__doc__)
    print(finder.Automate.__doc__)
    print(finder.BoyerMoore.__doc__)
    print(finder.KMP.__doc__)
    print(finder.SuffixArray.__doc__)

    grapher.build_graph()

    print(results_explanation)
    print()
    print(summary)

    sizes = [
        # (100000, 0),
        (100, 10),
        # (1000, 100),
        # (10000, 1000),
        # (100000, 100),
        # (1000000, 100),
    ]

    for text_size, pattern_size in sizes:
        text, pattern = Textgen('text.txt').generate(text_size)
        print(f'Generated: Text Length = {text_size}, '
              f'Pattern Size = {pattern_size}')
        results = [
            ('Brute Force',
             Chrono(finder.BruteForce).measure_accurate(text, pattern),
             Memo(finder.BruteForce).measure(text, pattern)),
            ('Hash Linear',
             Chrono(finder.Hash,
                    finder.Linear).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Linear).measure(text, pattern)),
            ('Hash Quad',
             Chrono(finder.Hash,
                    finder.Quad).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Quad).measure(text, pattern)),
            ('Hash RK',
             Chrono(finder.Hash,
                    finder.RabinKarph).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.RabinKarph).measure(text, pattern)),
            ('Automate',
             Chrono(finder.Automate).measure_accurate(text, pattern),
             Memo(finder.Automate).measure(text, pattern)),
            ('Boyer Moore',
             Chrono(finder.BoyerMoore).measure_accurate(text, pattern),
             Memo(finder.BoyerMoore).measure(text, pattern)),
            ('KMP',
             Chrono(finder.KMP).measure_accurate(text, pattern),
             Memo(finder.KMP).measure(text, pattern)),
            ('Suffix Array',
             Chrono(finder.SuffixArray).measure_accurate(text, pattern),
             Memo(finder.SuffixArray).measure(text, pattern)),
        ]
        results = sorted(results, key=lambda _: _[1])
        for name, time, memory in results:
            print(f'{name}\n\t%.6f S \n\t{memory} MB' % time)
        print(f'Best: {results[0]}')
        print(f'Worst: {results[-1]}')


if __name__ == '__main__':
    main()
