from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plot
import numpy as np
from chronograph import *
from textgen import *
from finder import *
import time


'''
def get_test_data(delta=0.05):

    from matplotlib.mlab import  bivariate_normal
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)

    Z1 = bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    Z2 = bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
    Z = Z2 - Z1

    X = X * 10
    Y = Y * 10
    Z = Z * 500
    return X, Y, Z

'''


def get_ndarrays(tuples3d, t_size, p_size, parts_count):
    p_base = -1
    x, y, z, = [], [], []
    count = 0
    for tuple in tuples3d:
        for t_size, p_size, time in tuple:
            if p_size != p_base:
                x.append([])
                y.append([])
                z.append([])
            x[count].append(t_size)
            y[count].append(p_size)
            z[count].append(time)
            count += 1
    # x = np.arange(0, t_size, 10)
    # y = np.arange(0, part_size, 1)
    # X, Y = np.meshgrid(x, y)
    X, Y = np.array(x), np.array(y)
    Z = np.array(z)
    return X, Y, Z


a = time.time()

brute_results = []
for i in range(1, 11):
    text_size = 100
    part_size = i
    part_count = 10
    text, pattern = Textgen('text.txt').generate(text_size, part_size)
    brute_results.append(
        Chronograph(BruteForce).measure_text_parts(text, pattern, part_count))

figure = plot.figure('NAME')
a1 = figure.add_subplot(111, projection='3d')
x, y, z = get_ndarrays(brute_results, 100, 10, 10)
a1.plot_wireframe(x, y, z, rstride=3, cstride=3)

# figure2 = plot.figure()
# a2 = figure2.add_subplot(111, projection='3d')
# a2.plot_surface(x, y, z, rstride=1, cstride=1)

print(time.time() - a)

plot.show()