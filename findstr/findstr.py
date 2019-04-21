import time as timer
import unittest
import inspect


class Result:
    def __init__(self, found_indexes, collisions=0, time=0.0, title=''):
        self.title = title
        self.found_indexes = found_indexes
        self.collisions = collisions
        self.time = time

    def log(self):
        print(f'       method {self.title}')
        print(f'     found on {self.found_indexes}')
        print(f'indexes count {len(self.found_indexes)}')
        print(f'   collisions {self.collisions}')
        print(f'         time {self.time}')
        print()


class Finder:
    class BruteForce:
        @staticmethod
        def search(text, sample):
            time_start = timer.time()

            found_indexes = []
            collisions = 0
            for i in range(len(text) - len(sample) + 1):
                logic = True
                for j in range(len(sample)):
                    if text[i + j] != sample[j]:
                        logic = False
                        collisions += 1
                        break
                if logic:
                    found_indexes.append(i)

            time_stop = timer.time()
            time = time_stop - time_start
            return Result(found_indexes, collisions, time,
                          Finder.BruteForce.__name__)

    class Hash:
        @staticmethod
        def search(text, sample, get_hash, hash_shift):
            time_start = timer.time()
            found_indexes = []
            sample_hash_sum = get_hash(sample, len(sample))
            subtext_hash_sum = get_hash(text, len(sample))
            collisions = 0

            for i in range(0, len(text) - len(sample) + 1):
                logic = True
                if i != 0:
                    subtext_hash_sum = hash_shift(i, len(sample),
                                                  subtext_hash_sum, text)

                if sample_hash_sum == subtext_hash_sum:
                    for j in range(0, len(sample)):
                        if text[i + j] != sample[j]:
                            logic = False
                            break
                    if logic:
                        found_indexes.append(i)
                    else:
                        collisions += 1

            time_stop = timer.time()
            time = time_stop - time_start
            return Result(found_indexes, collisions, time,
                          Finder.Hash.Linear.__name__)

        class Linear:
            @staticmethod
            def search(text, sample):
                return Finder.Hash.search(
                    text, sample,
                    Finder.Hash.Linear.get_hash,
                    Finder.Hash.Linear.hash_shift)

            @staticmethod
            def hash_shift(i, sample_length, current_hash, text):
                result = current_hash
                result -= ord(text[i - 1])
                result += ord(text[i + sample_length - 1])
                return result

            @staticmethod
            def get_hash(text, length):
                sum = 0
                for i in range(0, length):
                    if i < len(text):
                        sum += ord(text[i])
                return sum

        class Quad:
            @staticmethod
            def search(text, sample):
                return Finder.Hash.search(
                    text, sample,
                    Finder.Hash.Quad.get_hash,
                    Finder.Hash.Quad.hash_shift)

            @staticmethod
            def hash_shift(i, sample_length, current_hash, text):
                result = current_hash
                result -= ord(text[i - 1]) ** 2
                result += ord(text[i + sample_length - 1]) ** 2
                return result

            @staticmethod
            def get_hash(text, length):
                hash_sum = 0
                for i in range(0, length):
                    if i < len(text):
                        hash_sum += ord(text[i]) ** 2
                return hash_sum

        class RabinKarph:
            @staticmethod
            def search(text, sample):
                return Finder.Hash.search(
                    text, sample,
                    Finder.Hash.RabinKarph.get_hash,
                    Finder.Hash.RabinKarph.hash_shift)

            @staticmethod
            def hash_shift(i, length, current_hash, text):
                result = current_hash
                result -= ord(text[i - 1]) * (2 ** (length - 1))
                result *= 2
                result += ord(text[i + length - 1])
                return result

            @staticmethod
            def get_hash(text, length):
                hash_sum = 0
                for i in range(0, length):
                    if i < len(text):
                        hash_sum += ord(text[i]) * (2 ** (length - i - 1))
                return hash_sum

    class Automate:
        @staticmethod
        def search(text, sample):
            pass

    class BoyereMoore:
        @staticmethod
        def search(text, sample):
            pass


def main():
    pass


if __name__ == '__main__':
    main()


class Tester(unittest.TestCase):
    def assert_result(self, expected, actual, msg):
        self.assertTrue(hasattr(expected, 'found_indexes'))
        self.assertTrue(hasattr(actual, 'found_indexes'))

        self.assertListEqual(expected.found_indexes,
                             actual.found_indexes,
                             msg)

    def get_search_result_in_text(self, method, text, substring):
        self.assertTrue(hasattr(method, 'search'))
        return method.search(text, substring)

    def run_and_display(self, method, text, substr, testname, expected):
        with self.subTest(f'{method.__name__} on test \"{testname}\"'):
            actual = self.get_search_result_in_text(method, text, substr)
            self.assert_result(expected, actual, msg=f'\n{text}\n{substr}')

    @staticmethod
    def parse(test):
        data = test.readlines()
        answer = data[-1]
        text = data[0:len(data) - 1]
        return ''.join(str(line) for line in text), answer

    def test_all(self):
        methods = [Finder.BruteForce,
                   Finder.Hash.Linear,
                   Finder.Hash.Quad,
                   Finder.Hash.RabinKarph,
                   Finder.Automate,
                   Finder.BoyereMoore]
        tests_strings = [
            (
                '3 times substring',
                'aaa',
                'a',
                Result(
                    [0, 1, 2]
                )
            ),

            (
                '2 times substring',
                'aba',
                'a',
                Result(
                    [0, 2]
                )
            ),

            (
                'nothing found',
                'b',
                'a',
                Result(
                    []
                )
            ),

            (
                'nothing to search in',
                '',
                'a',
                Result(
                    []
                )
            ),

            (
                'one match',
                'a',
                'a',
                Result(
                    [0]
                )
            ),

            (
                'more than exists',
                'a',
                'aa',
                Result(
                    []
                )
            ),

            (
                'one 2 char match',
                'aa',
                'aa',
                Result(
                    [0]
                )
            ),

            (
                'triple overlay',
                'aaaa',
                'aa',
                Result(
                    [0, 1, 2]
                )
            ),

            (
                'double overlay',
                'aaaa',
                'aaa',
                Result(
                    [0, 1]
                )
            ),

            (
                'single match',
                'aaaba',
                'aaa',
                Result(
                    [0]
                )
            ),

            (
                'empty in empty',
                '',
                '',
                Result(
                    [0]
                )
            ),

            (
                'not found on last pos',
                'abcabcab',
                'abc',
                Result(
                    [0, 3]
                )
            ),

            (
                'template with separators',
                'ab ab ab',
                'ab',
                Result(
                    [0, 3, 6]
                )
            ),

            (
                'reverse repeated template',
                'ababababababababab',
                'bb',
                Result(
                    []
                )
            ),

            (
                'match',
                'abbaabbaabbbabaabaabbabbaabbbaabbabbbbbbaaaabbaaabbaaaaaabb',
                'aabba',
                Result(
                    [3, 17, 29, 42, 47]
                )
            ),

            (
                'no matches',
                'baabbbbbbababababaaaaabbaababbbabaaaabbbbaabbaaaaaabbabbaabbbbaab',
                'aaabab',
                Result(
                    []
                )
            ),

            (
                'chaotic',
                'abaababbbabababbbbabababbbabbabbabaabaababbaaaabbbbababaabb',
                'bbaba',
                Result(
                    [7, 16, 30, 49]
                )
            )
        ]

        tests_files = [
            ('big', 'tests/06.tst', 'tests/06.ans'),
            ('medium', 'tests/07.tst', 'tests/07.ans'),
            ('long', 'tests/08.tst', 'tests/08.ans'),
        ]

        for method in methods:
            # FIXME make a sub sub test group
            with self.subTest(f'{method.__name__} DONE'):
                for testname, text, substr, expected in tests_strings:
                    self.run_and_display(method, text, substr,
                                         testname, expected)

                for testname, file_test, file_ans in tests_files:
                    with open(file_test) as test:
                        text, substr = Tester.parse(test)
                        with open(file_ans) as answer:
                            indexes = []
                            for line in answer:
                                number = line[0:len(line) - 1]
                                if len(number) > 0:
                                    indexes.append(int(number))
                            expected = Result(indexes)
                            self.run_and_display(method, text, substr,
                                                 testname, expected)

