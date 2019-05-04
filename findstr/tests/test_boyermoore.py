import unittest
from finder import BoyerMoore
from tests_source import get_tests


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
