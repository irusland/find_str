def get_tests():
    return [
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