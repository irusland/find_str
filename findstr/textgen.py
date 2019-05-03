import unittest
import random


class Textgen:
    def __init__(self, *sources):
        if len(sources) == 0:
            raise ValueError('Source not found')
        self.text_sources = sources

    def generate(self, text_size, pattern_size=0):
        if text_size < pattern_size:
            raise IndexError
        is_word = pattern_size == 0
        rnd_text = ''
        while len(rnd_text) < text_size:
            pos = random.randint(0, len(self.text_sources) - 1)
            with open(self.text_sources[pos]) as t:
                text = t.read()
            a = random.randint(0, len(text))
            b = random.randint(0, len(text))
            rnd_text += text[min(a, b):max(a, b)]
        rnd_text = rnd_text[:text_size]
        yield rnd_text
        part = ''
        while len(part) < pattern_size:
            char = chr(random.randint(0, 255))
            split = rnd_text.split(char)
            part = split[random.randint(0, len(split) - 1)]

        if is_word:
            split = rnd_text.split(' ')
            pattern = split[random.randint(0, len(split) - 1)]
            while len(pattern) == 0:
                pattern = split[random.randint(0, len(split) - 1)]
            yield pattern
        else:
            i = random.randint(0, len(part))
            if i + pattern_size > len(part):
                yield part[len(part) - pattern_size:]
            else:
                yield part[i:i + pattern_size]


class Tester(unittest.TestCase):
    def test_text_word_generation(self):
        text_size = 10000
        gen = Textgen('text.txt')
        t, p = gen.generate(text_size)
        self.assertEqual(len(t), text_size)
        self.assertTrue(p in t)
        print(f'<P>{p}</P>')
        print(f'<T>{t}</T>')

    def test_text_substring_generation(self):
        text_size = 10000
        patten_size = 10
        gen = Textgen('text.txt')
        t, p = gen.generate(text_size, patten_size)
        self.assertEqual(len(t), text_size)
        self.assertEqual(len(p), patten_size, f'{p}')
        self.assertTrue(p in t)
        print(f'<P>{p}</P>')
        print(f'<T>{t}</T>')

    def test_text_substring_generation_small(self):
        text_size = 100
        patten_size = 1
        gen = Textgen('text.txt')
        t, p = gen.generate(text_size, patten_size)
        self.assertEqual(len(t), text_size)
        self.assertEqual(len(p), patten_size, f'{p}')
        self.assertTrue(p in t)
        print(f'<P>{p}</P>')
        print(f'<T>{t}</T>')
