import unittest
from textgen import Textgen


class Tester(unittest.TestCase):
    def test_text_word_generation(self):
        text_size = 10000
        gen = Textgen('text.txt')
        t, p = gen.generate(text_size)
        self.assertEqual(len(t), text_size)
        self.assertIn(p, t)
        print(f'<P>{p}</P>')
        print(f'<T>{t}</T>')

    def test_text_substring_generation(self):
        text_size = 10000
        patten_size = 10
        gen = Textgen('text.txt')
        t, p = gen.generate(text_size, patten_size)
        self.assertEqual(len(t), text_size)
        self.assertEqual(len(p), patten_size, f'{p}')
        self.assertIn(p, t)
        print(f'<P>{p}</P>')
        print(f'<T>{t}</T>')

    def test_text_substring_generation_small(self):
        text_size = 100
        patten_size = 1
        gen = Textgen('text.txt')
        t, p = gen.generate(text_size, patten_size)
        self.assertEqual(len(t), text_size)
        self.assertEqual(len(p), patten_size, f'{p}')
        self.assertIn(p, t)
        print(f'<P>{p}</P>')
        print(f'<T>{t}</T>')
