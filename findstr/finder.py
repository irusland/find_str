import time as timer
from result import *
import unittest


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
                      BruteForce.__name__)


class Hash:
    @staticmethod
    def search(text, sample, get_hash, hash_shift, name):
        time_start = timer.time()
        found_indexes = []
        sample_hash_sum = get_hash(sample, len(sample))
        subtext_hash_sum = get_hash(text, len(sample))
        collisions = 0

        for i in range(len(text) - len(sample) + 1):
            logic = True
            if i != 0:
                subtext_hash_sum = hash_shift(i, len(sample),
                                              subtext_hash_sum, text)

            if sample_hash_sum == subtext_hash_sum:
                for j in range(len(sample)):
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
            return Hash.search(
                text, sample,
                Hash.Linear.get_hash,
                Hash.Linear.hash_shift, 'Linear')

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
        def search(text, sample):
            return Hash.search(
                text, sample,
                Hash.Quad.get_hash,
                Hash.Quad.hash_shift, 'Quad')

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
        def search(text, sample):
            return Hash.search(
                text, sample,
                Hash.RabinKarph.get_hash,
                Hash.RabinKarph.hash_shift, 'Rabin Karph')

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


class Automate:
    @staticmethod
    def search(text, sample):
        time_start = timer.time()

        found_indexes = []
        collisions = 0
        length = len(sample)
        alphabet = {}

        for i in range(length):
            alphabet[sample[i]] = 0

        table = {}
        for j in range(length + 1):
            table[j] = {}

        for i in alphabet:
            table[0][i] = 0

        for j in range(length):
            prev = table[j][sample[j]]
            table[j][sample[j]] = j + 1
            for i in alphabet:
                table[j + 1][i] = table[prev][i]

        current_state = 0
        sample_length = len(sample)
        for i in range(len(text)):
            if text[i] not in table[current_state]:
                collisions += 1
                current_state = 0
                continue
            current_state = table[current_state][text[i]]
            if current_state == sample_length:
                found_indexes.append(i - sample_length + 1)

        time_stop = timer.time()
        time = time_stop - time_start
        return Result(found_indexes, collisions, time, 'Automate')


class BoyereMoore:
    @staticmethod
    def get_table_of_last_char_appearance(pattern):
        table = {}
        m = len(pattern)
        for i in range(m - 1):
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
        for p in range(m + 1):
            for k in range(m - p + 1, -m, -1):
                is_bs = BoyereMoore.is_equal(
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
        for l in range(m + 1):
            shift[l] = m - rpr[l] - l + 1
        return shift

    @staticmethod
    def search(text, pattern):
        time_start = timer.time()

        bc_table = BoyereMoore.get_table_of_last_char_appearance(pattern)
        rpr = BoyereMoore.get_rpr_table(pattern)
        gs_table = BoyereMoore.get_shift_table(rpr, pattern)

        collisions = 0
        m = len(pattern)
        i = 0
        match_streak = 0
        execute = True
        indexes = []
        while execute:
            if pattern == '':
                for s in range(text.length):
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
        return Result(indexes, collisions, time, 'Boyer moore')


class KMP:
    @staticmethod
    def partial(pattern):
        table = [0]
        for i in range(1, len(pattern)):
            j = table[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = table[j - 1]
            if pattern[j] == pattern[i]:
                table.append(j + 1)
            else:
                table.append(j)
        return table

    @staticmethod
    def search(text, pattern):
        time_start = timer.time()

        partial = KMP.partial(pattern)
        indexes = []
        collisions = 0
        j = 0

        for i in range(len(text)):
            while j > 0 and text[i] != pattern[j]:
                collisions += 1
                j = partial[j - 1]
            if text[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                indexes.append(i - (j - 1))
                j = partial[j - 1]

        time_stop = timer.time()
        time = time_stop - time_start
        return Result(indexes, collisions, time, "KMP")


class SuffixArray:
    @staticmethod
    def build_suffix_array(text):
        suffixes = []
        for i in range(len(text)):
            suffix = text[-(i + 1):]
            suffixes.append((suffix, len(text) - i))
        suffixes.sort(key=lambda tup: tup[0])
        return suffixes

    @staticmethod
    def search(text, pattern):
        pass

    class Tester(unittest.TestCase):
        def test_suffix_array_banana(self):
            arr = SuffixArray.build_suffix_array('banana')
            self.assertListEqual([('a', 6),
                                  ('ana', 4),
                                  ('anana', 2),
                                  ('banana', 1),
                                  ('na', 5),
                                  ('nana', 3)], arr)

        def test_suffix_array_abaab(self):
            arr = SuffixArray.build_suffix_array('abaab')
            self.assertListEqual([('aab', 3),
                                  ('ab', 4),
                                  ('abaab', 1),
                                  ('b', 5),
                                  ('baab', 2)], arr)