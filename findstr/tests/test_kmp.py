import unittest
from finder import KMP
from tests_source import get_tests


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
