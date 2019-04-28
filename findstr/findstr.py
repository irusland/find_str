from tkinter import *
import math
from chronograph import *
from textgen import *
from finder import *

root = Tk()
root.title('grapher')
root.geometry('1020x620')

canvas = Canvas(root, width=1020, height=620, bg='#999')

for y in range(21):
    k = 50 * y
    canvas.create_line(10+k, 610, 10+k, 10, width=1, fill='#191938')

for x in range(13):
    k = 50 * x
    canvas.create_line(10, 10+k, 1010, 10+k, width=1, fill='#191938')

canvas.create_line(60, 10, 60, 610, width=1, arrow=FIRST, fill='white')
canvas.create_line(0, 560, 1010, 560, width=1, arrow=LAST, fill='white')

text_size = 10000
part_count = 10
text, pattern = Textgen('text.txt').generate(text_size)
bruteforce = Chronograph(BruteForce).measure_text_parts(text, pattern, part_count)

xy = []
for length, m, time in bruteforce:
    x = length / 10
    y = -(time * 1000000) + 310
    xy.append(x)
    xy.append(y)

sin_line = canvas.create_line(xy, fill='red')

canvas.pack()
root.mainloop()
