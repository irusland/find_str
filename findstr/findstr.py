#!/usr/bin/python3.6

import unittest
from finder import *
from result import *


def main():
    methods = [
        BruteForce,
        # Hash.Linear,
        # Hash.Quad,
        # Hash.RabinKarph,
        Automate,
        BoyerMoore,
        KMP
    ]
    for method in methods:
        result = method('aa').search('aaaa')
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

    def get_search_result_in_text(self, method, text, pattern,
                                  hash_method=None):
        self.assertTrue(hasattr(method, 'search'))
        if hash_method is not None:
            return method(pattern, hash_method).search(text)
        return method(pattern).search(text)

    def run_and_display(self, method, text, sub_string, test_name, expected,
                        hash_method=None):
        with self.subTest(f'{method.__name__}.{hash_method} '
                          f'on test \"{test_name}\"'):
            if hash_method is not None:
                actual = self.get_search_result_in_text(
                    method, text, sub_string, hash_method)
            else:
                actual = self.get_search_result_in_text(
                    method, text, sub_string)
            msg = f'\nTEXT: {text} :TEXT\nSUB: {sub_string} :SUB'
            self.assert_result(expected, actual, msg)

    @staticmethod
    def parse(test):
        data = test.readlines()
        answer = data[-1]
        text = data[:-1]
        text_str = ''.join(map(str, text))[:-1]
        text_str = text_str[:-1]
        return text_str, answer

    def test_all(self):
        methods = [
            BruteForce,
            Hash,
            Automate,
            BoyerMoore,
            KMP
        ]
        hash_methods = [
            Hash.Linear,
            Hash.Quad,
            Hash.RabinKarph
        ]
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
            with self.subTest(f'{method.__name__} DONE'):
                for test_name, text, sub_string, expected in tests_strings:
                    if method.__name__ == 'Hash':
                        for hash_method in hash_methods:
                            self.run_and_display(method, text, sub_string,
                                                 test_name, Result(expected),
                                                 hash_method)
                    else:
                        self.run_and_display(method, text, sub_string,
                                             test_name, Result(expected))

                for test_name, file_test, file_ans in tests_files:
                    with open(file_test) as test:
                        text, sub_string = Tester.parse(test)
                        with open(file_ans) as answer:
                            indexes = []
                            for line in answer:
                                number = line[:-1]
                                if len(number) > 0:
                                    indexes.append(int(number))
                            expected = Result(indexes)
                            if method.__name__ == 'Hash':
                                for hash_method in hash_methods:
                                    self.run_and_display(method, text,
                                                         sub_string,
                                                         test_name,
                                                         expected,
                                                         hash_method)
                            else:
                                self.run_and_display(method, text, sub_string,
                                                     test_name, expected)
