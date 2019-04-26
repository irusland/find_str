import time as timer
import unittest


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
        def search(text, sample, get_hash, hash_shift, name):
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
            return Result(found_indexes, collisions, time, name)

        class Linear:
            @staticmethod
            def search(text, sample):
                return Finder.Hash.search(
                    text, sample,
                    Finder.Hash.Linear.get_hash,
                    Finder.Hash.Linear.hash_shift, 'Linear')

            @staticmethod
            def hash_shift(i, sample_length, current_hash, text):
                result = current_hash
                result -= ord(text[i - 1])
                result += ord(text[i + sample_length - 1])
                return result

            @staticmethod
            def get_hash(text, length):
                hash_sum = 0
                for i in range(0, length):
                    if i < len(text):
                        hash_sum += ord(text[i])
                return hash_sum

        class Quad:
            @staticmethod
            def search(text, sample):
                return Finder.Hash.search(
                    text, sample,
                    Finder.Hash.Quad.get_hash,
                    Finder.Hash.Quad.hash_shift, 'Quad')

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
                    Finder.Hash.RabinKarph.hash_shift, 'Rabin Karph')

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
            title = 'Automate'
            time_start = timer.time()

            found_indexes = []
            collisions = 0
            length = len(sample)
            alphabet = {}

            for i in range(0, length):
                alphabet[sample[i]] = 0

            table = {}
            for j in range(0, length + 1):
                table[j] = {}

            for i in alphabet:
                table[0][i] = 0

            for j in range(0, length):
                prev = table[j][sample[j]]
                table[j][sample[j]] = j + 1
                for i in alphabet:
                    table[j + 1][i] = table[prev][i]

            current_state = 0
            sample_length = len(sample)
            for i in range(0, len(text)):
                if text[i] not in table[current_state].keys():
                    collisions += 1
                    current_state = 0
                    continue
                current_state = table[current_state][text[i]]
                if current_state == sample_length:
                    found_indexes.append(i - sample_length + 1)

            time_stop = timer.time()
            time = time_stop - time_start
            return Result(found_indexes, collisions, time, title)

    class BoyereMoore:
        @staticmethod
        def get_table_of_last_char_appearance(pattern):
            table = {}
            m = len(pattern)
            for i in range(0, m - 1):
                table[pattern[i]] = m - 1 - i
            return table

        @staticmethod
        def is_equal(str1, a, b, str2, m):
            for k in range(a, b + 1):
                if str1[k] == '*':
                    m += 1
                    continue
                if str1[k] != str2[m]:
                    return False
                else:
                    m += 1
            return True

        @staticmethod
        def get_rpr_table(t):
            m = len(t)
            rpr = {}
            tx = ('*' * len(t)) + t
            for p in range(0, m + 1):
                for k in range(m - p + 1, 1 - m - 1, -1):
                    is_bs = Finder.BoyereMoore.is_equal(
                        tx, k + m - 1, k + m + p - 2, t, m - p)
                    if (is_bs and ((k - 2 >= 0 and t[k - 2] != t[m - p - 1])
                                   or k - 2 < 0) and (p != m or k != 1)):
                        rpr[p] = k
                        break
            return rpr

        @staticmethod
        def get_shift_table(rpr, pattern):
            m = len(pattern)
            shift = {}
            for l in range(0, m + 1):
                shift[l] = m - rpr[l] - l + 1
            return shift

        @staticmethod
        def search(text, pattern):
            title = 'Boyer moore'
            time_start = timer.time()

            bc_table = \
                Finder.BoyereMoore.get_table_of_last_char_appearance(pattern)
            rpr = Finder.BoyereMoore.get_rpr_table(pattern)
            gs_table = Finder.BoyereMoore.get_shift_table(rpr, pattern)

            collisions = 0
            m = len(pattern)
            i = 0
            match_streak = 0
            execute = True
            indexes = []
            while execute:
                if pattern == '':
                    for s in range(0, text.length):
                        indexes.append(s)
                    execute = False
                if i + m > len(text):
                    break
                for j in range(i + m - 1, i - 1, -1):
                    if text[j] == pattern[j - i]:
                        match_streak += 1
                        if match_streak == m:
                            indexes.append(i)
                            i += gs_table[match_streak]
                            match_streak = 0
                            break
                    else:
                        if match_streak == 0:
                            if text[j] not in bc_table.keys():
                                i += m
                            else:
                                i += bc_table[text[j]]
                        else:
                            collisions += 1
                            i += gs_table[match_streak]
                        match_streak = 0
                        break

            time_stop = timer.time()
            time = time_stop - time_start

            return Result(indexes, collisions, time, title)


def main():
    methods = [
        Finder.BruteForce,
        Finder.Hash.Linear,
        Finder.Hash.Quad,
        Finder.Hash.RabinKarph,
        Finder.Automate,
        Finder.BoyereMoore
    ]
    for method in methods:
        result = method.search('A', 'A')
        result.log()


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

    def run_and_display(self, method, text, sub_string, test_name, expected):
        with self.subTest(f'{method.__name__} on test \"{test_name}\"'):
            actual = self.get_search_result_in_text(method, text, sub_string)
            msg = f'\nTEXT: {text} :TEXT\nSUB: {sub_string} :SUB'
            self.assert_result(expected, actual, msg)

    @staticmethod
    def parse(test):
        data = test.readlines()
        answer = data[-1]
        text = data[0:len(data) - 1]
        text_str = ''.join(str(line) for line in text)
        text_str = text_str[0:len(text_str) - 1]
        return text_str, answer

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
                [0, 1, 2]
            ),

            (
                '2 times substring',
                'aba',
                'a',
                [0, 2]
            ),

            (
                'nothing found',
                'b',
                'a',
                []
            ),

            (
                'nothing to search in',
                '',
                'a',
                []
            ),

            (
                'one match',
                'a',
                'a',
                [0]
            ),

            (
                'more than exists',
                'a',
                'aa',
                []
            ),

            (
                'one 2 char match',
                'aa',
                'aa',
                [0]
            ),

            (
                'triple overlay',
                'aaaa',
                'aa',
                [0, 1, 2]
            ),

            (
                'double overlay',
                'aaaa',
                'aaa',
                [0, 1]
            ),

            (
                'single match',
                'aaaba',
                'aaa',
                [0]
            ),

            (
                'not found on last pos',
                'abcabcab',
                'abc',
                [0, 3]
            ),

            (
                'template with separators',
                'ab ab ab',
                'ab',
                [0, 3, 6]
            ),

            (
                'reverse repeated template',
                'ababababababababab',
                'bb',
                []
            ),

            (
                'match',
                'abbaabbaabbbabaabaabbabbaabbbaabbabbbbbbaaaabbaaabbaaaaaabb',
                'aabba',
                [3, 17, 29, 42, 47]
            ),

            (
                'no matches',
                'baabbbbbbababababaaaaabbaababbbabaa'
                'aabbbbaabbaaaaaabbabbaabbbbaab',
                'aaabab',
                []
            ),

            (
                'chaotic',
                'abaababbbabababbbbabababbbabbabbabaabaababbaaaabbbbababaabb',
                'bbaba',
                [7, 16, 30, 49]
            )
        ]

        tests_files = [
            ('big', 'tests/06.tst', 'tests/06.ans'),
            ('medium', 'tests/07.tst', 'tests/07.ans'),
            ('long', 'tests/08.tst', 'tests/08.ans')
        ]

        for method in methods:
            # FIXME make a sub sub test group
            with self.subTest(f'{method.__name__} DONE'):
                for test_name, text, sub_string, expected in tests_strings:
                    self.run_and_display(method, text, sub_string,
                                         test_name, Result(expected))

                for test_name, file_test, file_ans in tests_files:
                    with open(file_test) as test:
                        text, sub_string = Tester.parse(test)
                        with open(file_ans) as answer:
                            indexes = []
                            for line in answer:
                                number = line[0:len(line) - 1]
                                if len(number) > 0:
                                    indexes.append(int(number))
                            expected = Result(indexes)
                            self.run_and_display(method, text, sub_string,
                                                 test_name, expected)


# ВЫЧИСТИТЬ АРХИВ