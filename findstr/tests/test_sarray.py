import unittest
from finder import SuffixArray
from tests_source import get_tests


class SarrayTester(unittest.TestCase):
    def test_search(self):
        for test_name, text, pattern, expected in get_tests():
            with self.subTest(f'{test_name}'):
                actual = SuffixArray(text).search(pattern)
                msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                self.assertCountEqual(expected, actual.found_indexes, msg)

    def test_bananana(self):
        arr = SuffixArray.build_suffix_array('bananana')
        self.assertListEqual([('a', 7),
                              ('ana', 5),
                              ('anana', 3),
                              ('ananana', 1),
                              ('bananana', 0),
                              ('na', 6),
                              ('nana', 4),
                              ('nanana', 2)], arr)
        res = SuffixArray('bananana').search('ana')
        self.assertListEqual(res.found_indexes, [1, 3, 5])

    def test_banana(self):
        arr = SuffixArray.build_suffix_array('banana')
        self.assertListEqual([('a', 5),
                              ('ana', 3),
                              ('anana', 1),
                              ('banana', 0),
                              ('na', 4),
                              ('nana', 2)], arr)
        res = SuffixArray('banana').search('ana')
        self.assertListEqual(res.found_indexes, [1, 3])

    def test_abaab(self):
        arr = SuffixArray.build_suffix_array('abaab')
        self.assertListEqual([('aab', 2),
                              ('ab', 3),
                              ('abaab', 0),
                              ('b', 4),
                              ('baab', 1)], arr)
        res = SuffixArray('abaab').search('ab')
        self.assertListEqual(res.found_indexes, [0, 3])

