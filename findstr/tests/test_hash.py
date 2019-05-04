import unittest
from finder import Hash, Linear, Quad, RabinKarph
from tests_source import get_tests


class HashTester(unittest.TestCase):
    def test_search(self):
        hash_methods = [
            Linear,
            Quad,
            RabinKarph
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
                actual = Linear.get_hash(pattern, len(pattern))
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
                actual = Quad.get_hash(pattern, len(pattern))
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
                actual = RabinKarph.get_hash(pattern, len(pattern))
                self.assertEqual(result, actual)
