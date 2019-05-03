import collections
import time as timer
from result import *
import unittest
from tests_source import *


class BruteForce:
    """
    Brute Force algorithm associated simply comparing every
    substring char and pattern char until match
    """

    def __init__(self, pattern):
        self.pattern = pattern

    def search(self, text):
        found_indexes = []
        collisions = 0
        for i in range(len(text) - len(self.pattern) + 1):
            logic = True
            for j in range(len(self.pattern)):
                if text[i + j] != self.pattern[j]:
                    logic = False
                    collisions += 1
                    break
            if logic:
                found_indexes.append(i)
        return Result(found_indexes, collisions, BruteForce.__name__)


class BruteForceTester(unittest.TestCase):
    def test(self):
        for test_name, text, pattern, expected in get_tests():
            with self.subTest(f'{test_name}'):
                actual = BruteForce(pattern).search(text).found_indexes
                msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                self.assertListEqual(expected, actual, msg)


class Hash:
    """
    Hashing algorithm based on summarizing chars ordinals with a special
    function to simplify strings comparison
    """

    def __init__(self, pattern, hash_method):
        self.pattern = pattern
        self.hash_method = hash_method

    def search(self, text):
        found_indexes = []
        sample_hash_sum = \
            self.hash_method.get_hash(self.pattern, len(self.pattern))
        subtext_hash_sum = self.hash_method.get_hash(text, len(self.pattern))
        collisions = 0

        for i in range(len(text) - len(self.pattern) + 1):
            full_match = True
            if i != 0:
                subtext_hash_sum = self.hash_method.hash_shift(
                    i, len(self.pattern), subtext_hash_sum, text)

            if sample_hash_sum == subtext_hash_sum:
                for j in range(len(self.pattern)):
                    if text[i + j] != self.pattern[j]:
                        full_match = False
                        break
                if full_match:
                    found_indexes.append(i)
                else:
                    collisions += 1
        return Result(
            found_indexes, collisions, self.hash_method.__name__)

    class Linear:
        @staticmethod
        def hash_shift(i, sample_length, current_hash, text):
            result = current_hash
            result -= ord(text[i - 1])
            result += ord(text[i + sample_length - 1])
            return result

        @staticmethod
        def get_hash(text, length):
            hash_sum = 0
            for i in range(length):
                if i < len(text):
                    hash_sum += ord(text[i])
            return hash_sum

    class Quad:
        @staticmethod
        def hash_shift(i, sample_length, current_hash, text):
            result = current_hash
            result -= ord(text[i - 1]) ** 2
            result += ord(text[i + sample_length - 1]) ** 2
            return result

        @staticmethod
        def get_hash(text, length):
            hash_sum = 0
            for i in range(length):
                if i < len(text):
                    hash_sum += ord(text[i]) ** 2
            return hash_sum

    class RabinKarph:
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
            for i in range(length):
                if i < len(text):
                    hash_sum += ord(text[i]) * (2 ** (length - i - 1))
            return hash_sum


class HashTester(unittest.TestCase):
    def test_search(self):
        hash_methods = [
            Hash.Linear,
            Hash.Quad,
            Hash.RabinKarph
        ]
        for test_name, text, pattern, expected in get_tests():
            for hash_method in hash_methods:
                with self.subTest(f'{hash_method.__name__} {test_name}'):
                    actual = Hash(pattern, hash_method).search(text)
                    msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                    self.assertListEqual(expected, actual.found_indexes, msg)

    def test_linear_hash(self):
        hash_source = [
            ('', 0),
            ('a', 97),
            ('aaa', 291),
            ('abc', 294)
        ]
        for pattern, result in hash_source:
            with self.subTest(f'{pattern}'):
                actual = Hash.Linear.get_hash(pattern, len(pattern))
                self.assertEqual(result, actual)

    def test_quad_hash(self):
        hash_source = [
            ('', 0),
            ('a', 9409),
            ('aaa', 28227),
            ('abc', 28814)
        ]
        for pattern, result in hash_source:
            with self.subTest(f'{pattern}'):
                actual = Hash.Quad.get_hash(pattern, len(pattern))
                self.assertEqual(result, actual)

    def test_rk_hash(self):
        hash_source = [
            ('', 0),
            ('a', 97),
            ('aaa', 679),
            ('abc', 683)
        ]
        for pattern, result in hash_source:
            with self.subTest(f'{pattern}'):
                actual = Hash.RabinKarph.get_hash(pattern, len(pattern))
                self.assertEqual(result, actual)


class Automate:
    """
    Automate algorithm has a preprocessing component it builds a table of
    shifts out of pattern which is used during method execution
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.table = self.get_table()

    def get_table(self):
        length = len(self.pattern)
        alphabet = []
        table = collections.defaultdict(collections.defaultdict)

        for i in range(length):
            alphabet.append(self.pattern[i])
        for i in alphabet:
            table[0][i] = 0

        for j in range(length):
            prev = table[j][self.pattern[j]]
            table[j][self.pattern[j]] = j + 1
            for i in alphabet:
                table[j + 1][i] = table[prev][i]
        return table

    def search(self, text):
        found_indexes = []
        collisions = 0
        current_state = 0
        sample_length = len(self.pattern)
        for i in range(len(text)):
            if text[i] not in self.table[current_state]:
                collisions += 1
                current_state = 0
                continue
            current_state = self.table[current_state][text[i]]
            if current_state == sample_length:
                found_indexes.append(i - sample_length + 1)

        return Result(found_indexes, collisions, 'Automate')


class AutomateTester(unittest.TestCase):
    def test_search(self):
        for test_name, text, pattern, expected in get_tests():
            with self.subTest(f'{test_name}'):
                actual = Automate(pattern).search(text)
                msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                self.assertListEqual(expected, actual.found_indexes, msg)

    def test_table(self):
        table_source = [
            ('', {}),
            ('a', {0: {'a': 1}, 1: {'a': 1}}),
            ('aaa', {0: {'a': 1}, 1: {'a': 2}, 2: {'a': 3}, 3: {'a': 3}}),
            ('abc', {0: {'a': 1, 'b': 0, 'c': 0},
                     1: {'a': 1, 'b': 2, 'c': 0},
                     2: {'a': 1, 'b': 0, 'c': 3},
                     3: {'a': 1, 'b': 0, 'c': 0}})
        ]
        for pattern, result in table_source:
            with self.subTest(f'{pattern}'):
                actual = Automate(pattern).get_table()
                self.assertDictEqual(result, actual)


class BoyerMoore:
    """
    Boyer Moore algorithm preprocess a pattern and builds shift tables for
    "bad char" anb "good suffix" heuristics
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.tx = ('*' * len(self.pattern)) + self.pattern
        self.bc_table = self.get_table_of_last_char_appearance()
        self.rpr = self.get_rpr_table()
        self.gs_table = self.get_shift_table()

    def get_table_of_last_char_appearance(self):
        m = len(self.pattern) - 1
        return {c: (m - i) for (i, c) in enumerate(self.pattern)}

    def is_equal(self, a, b, m):
        for k in range(a, b):
            if self.tx[k] == '*':
                m += 1
                continue
            if self.tx[k] != self.pattern[m]:
                return False
            else:
                m += 1
        return True

    def get_rpr_table(self):
        m = len(self.pattern)
        rpr = {}
        for p in range(m + 1):
            for k in range(m - p + 1, -m, -1):
                is_bad_suffix = self.is_equal(k + m - 1, k + m + p - 1, m - p)
                if (is_bad_suffix and ((k - 2 >= 0 and self.pattern[k - 2]
                                       != self.pattern[m - p - 1])
                                       or k - 2 < 0) and (p != m or k != 1)):
                    rpr[p] = k
                    break
        return rpr

    def get_shift_table(self):
        m = len(self.pattern)
        shift = {}
        for l in range(m + 1):
            shift[l] = m - self.rpr[l] - l + 1
        return shift

    def search(self, text):
        collisions = 0
        m = len(self.pattern)
        i = 0
        match_streak = 0
        execute = True
        indexes = []
        while execute:
            if self.pattern == '':
                for s in range(text.length):
                    indexes.append(s)
                execute = False
            if i + m > len(text):
                break
            for j in range(i + m - 1, i - 1, -1):
                if text[j] == self.pattern[j - i]:
                    match_streak += 1
                    if match_streak == m:
                        indexes.append(i)
                        i += self.gs_table[match_streak]
                        match_streak = 0
                        break
                else:
                    if match_streak == 0:
                        if text[j] not in self.bc_table.keys():
                            i += m
                        else:
                            i += self.bc_table[text[j]]
                    else:
                        collisions += 1
                        i += self.gs_table[match_streak]
                    match_streak = 0
                    break
        return Result(indexes, collisions, 'Boyer moore')


class BoyerMooreTester(unittest.TestCase):
    def test_search(self):
        for test_name, text, pattern, expected in get_tests():
            with self.subTest(f'{test_name}'):
                actual = BoyerMoore(pattern).search(text)
                msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                self.assertListEqual(expected, actual.found_indexes, msg)

    def test_bc_table(self):
        table_source = [
            ('a', {'a': 0}),
            ('aaa', {'a': 0}),
            ('abc', {'a': 2, 'b': 1, 'c': 0})
        ]
        for pattern, result in table_source:
            with self.subTest(f'{pattern}'):
                actual = BoyerMoore(pattern).bc_table
                self.assertDictEqual(result, actual)

    def test_gs_table(self):
        table_source = [
            ('a', {0: 1, 1: 1}),
            ('aaa', {0: 3, 1: 2, 2: 1, 3: 1}),
            ('abc', {0: 1, 1: 3, 2: 3, 3: 3})
        ]
        for pattern, result in table_source:
            with self.subTest(f'{pattern}'):
                actual = BoyerMoore(pattern).gs_table
                self.assertDictEqual(result, actual)

    def test_rpr_table(self):
        table_source = [
            ('a', {0: 1, 1: 0}),
            ('aaa', {0: 1, 1: 1, 2: 1, 3: 0}),
            ('abc', {0: 3, 1: 0, 2: -1, 3: -2})
        ]
        for pattern, result in table_source:
            with self.subTest(f'{pattern}'):
                actual = BoyerMoore(pattern).rpr
                self.assertDictEqual(result, actual)


class KMP:
    """
    KMP or Knuth-Morris-Pratt's algorithm builds shift table with least common
    subsequence method then uses it during search
    """

    def __init__(self, pattern):
        self.pattern = pattern
        self.partial = self.partial()

    def partial(self):
        table = [0]
        for i in range(1, len(self.pattern)):
            j = table[i - 1]
            while j > 0 and self.pattern[j] != self.pattern[i]:
                j = table[j - 1]
            if self.pattern[j] == self.pattern[i]:
                table.append(j + 1)
            else:
                table.append(j)
        return table

    def search(self, text):
        indexes = []
        collisions = 0
        j = 0

        for i in range(len(text)):
            while j > 0 and text[i] != self.pattern[j]:
                collisions += 1
                j = self.partial[j - 1]
            if text[i] == self.pattern[j]:
                j += 1
            if j == len(self.pattern):
                indexes.append(i - (j - 1))
                j = self.partial[j - 1]

        return Result(indexes, collisions, "KMP")


class KMPTester(unittest.TestCase):
    def test_search(self):
        for test_name, text, pattern, expected in get_tests():
            with self.subTest(f'{test_name}'):
                actual = KMP(pattern).search(text)
                msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                self.assertListEqual(expected, actual.found_indexes, msg)

    def test_table(self):
        table_source = [
            ('a', [0]),
            ('aaa', [0, 1, 2]),
            ('abc', [0, 0, 0])
        ]
        for pattern, result in table_source:
            with self.subTest(f'{pattern}'):
                actual = KMP(pattern).partial
                self.assertListEqual(result, actual)
