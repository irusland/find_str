from chronograph import Chronograph
import unittest
import finder
from textgen import Textgen


class ChronoTester(unittest.TestCase):
    def test_open(self):
        c = Chronograph('')
        t, p = c.open_file()
        self.assertEqual(len(p), 5)
        self.assertGreater(len(t), 100)

    def test_measure(self):
        c = Chronograph(finder.Hash, finder.Linear)
        t, p = c.open_file()
        time = c.measure(t, p)
        self.assertNotEqual(time, 0)

    def test_measure_accurate_small(self):
        c = Chronograph(finder.Hash, finder.Linear)
        t, p = 'aaabbbaba', 'ab'
        times = [c.measure_accurate(t, p) for _ in range(10)]
        base_time = times[0]
        count = 1
        for time in times:
            self.assertAlmostEqual(time, base_time, delta=1e-5)
            base_time *= count
            base_time += time
            count += 1
            base_time /= count

    def test_measure_accurate_big(self):
        c = Chronograph(finder.Hash, finder.Linear)
        t, p = c.open_file()
        times = []
        for i in range(3):
            times.append(c.measure_accurate(t, p))
        base_time = times[0]
        count = 1
        for time in times:
            self.assertAlmostEqual(time, base_time, delta=1e-1)
            base_time *= count
            base_time += time
            count += 1
            base_time /= count

    def test_measure_text_parts(self):
        c = Chronograph(finder.Hash, finder.Linear)
        t, p = Textgen('text.txt').generate(1000)
        part_times = c.measure_text_parts(t, p, 3)
        count = 0
        current = (0, 0, 0)
        for part in part_times:
            self.assertLess(current[0], part[0], f'{current[0]} < {part[0]}')
            self.assertLess(current[2], part[2], f'{current[2]} < {part[2]}')
            count += 1
            current = part
        self.assertEqual(count, 3,
                         f'len(part_times) == {count}\n {part_times}')
