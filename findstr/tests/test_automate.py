import unittest
from finder import Automate
from tests_source import get_tests


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
