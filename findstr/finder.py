import collections
from result import Result


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


class Hash:
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
    """
    Hashing algorithm based on summarizing chars ordinals
    to simplify strings comparison
    """
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
    """
    Hashing algorithm based on summarizing chars ordinals in square
    to simplify strings comparison
    """
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
    """
    Hashing algorithm based on summarizing chars ordinals with special
    Rabin Karph formula to simplify strings comparison
    """
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


class SuffixArray:
    """
    Suffix Array algorithm preprocess a text string with making a suffix
    array then uses a binary search to find left and right answer borders
    """
    def __init__(self, pattern):
        self.pattern = pattern

    @staticmethod
    def build_suffix_array(text):
        suffixes = []
        for i in range(len(text)):
            suffix = text[-(i + 1):]
            suffixes.append((suffix, len(text) - i - 1))
        suffixes.sort(key=lambda tup: tup[0])
        return suffixes

    def left_border(self, sarray):
        left = -1
        right = len(sarray)
        while left < right:
            m = int(left + (right - left) / 2)
            if left + 1 == right:
                break
            if sarray[m][0] >= self.pattern:
                right = m
            if sarray[m][0] < self.pattern:
                left = m
        return left

    def right_border(self, sarray):
        left = -1
        right = len(sarray)
        while left < right:
            m = int(left + (right - left) / 2)
            if left + 1 == right:
                break
            if sarray[m][0] >= self.pattern:
                if sarray[m][0].startswith(self.pattern):
                    left = m
                else:
                    right = m
            else:
                left = m

        return right

    def search(self, text):
        sarray = self.build_suffix_array(text)
        left = self.left_border(sarray)
        right = self.right_border(sarray)

        return Result([sarray[i][1] for i in range(right - 1, left, -1)],
                      0, "Suffix Array")
