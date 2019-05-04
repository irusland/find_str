import unittest
from finder import BruteForce
from tests_source import get_tests


class BruteForceTester(unittest.TestCase):
    def test(self):
        for test_name, text, pattern, expected in get_tests():
            with self.subTest(f'{test_name}'):
                actual = BruteForce(pattern).search(text).found_indexes
                msg = f'\nTEXT: {text} :TEXT\nSUB: {pattern} :SUB'
                self.assertListEqual(expected, actual, msg)