#!/usr/bin/env python

from __future__ import print_function
from matplotlib import pyplot as pyplot, pylab as pylab
from scipy import stats
import numpy as np
from os import path

RESULTS_BASE_DIR = 'results'
RESULTS_FILE = path.join(RESULTS_BASE_DIR, 'results.json')


def plot_averages_with_sdvs(data, x_label, y_label, title):
    '''
    Data is a two dimensional array with the data arrays for every class.
    Title is the title of the plot as string.
    y_label is y label as string.
    x_label tuple of strings for y label same length as data.
    '''
    x_mean = []
    x_std = []
    width = 0.35

    for e in data:
        x_mean.append(np.mean(e))
        x_std.append(np.std(e))

    ind = np.arange(len(x_mean))
    pyplot.figure()
    pyplot.title(title)
    for i in range(len(x_mean)):
        pyplot.bar(ind[i], x_mean[i], width, align='center', yerr=x_std[i], ecolor='k')
    pyplot.ylabel(y_label)
    pyplot.xticks(ind, x_label)
    pyplot.show()


def plot_regression_line_with_pointcloud(data, x_label, y_label, title, classes):
    fig = pyplot.figure()
    ax1 = fig.add_subplot(121)
    ax1.title(title)

    data_x, data_y = zip(*data[0])
    ax1.scatter(data_x, data_y)


def main():
    import numpy as np
    import matplotlib.pyplot as plt
    import json

    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)
    n_sims = len(data) / 2

    print("Loaded %i keys from results file, assuming %i simulation pairs" % (len(data), n_sims))

    with_lists, without_lists = [], []
    for i in xrange(1, n_sims + 1):
        key_pfx = "sim_%i" % i
        with_lists.append(data[key_pfx + "T"])
        without_lists.append(data[key_pfx + "F"])

    with_stacked, without_stacked = np.vstack(with_lists), np.vstack(without_lists)
    with_means, without_means = np.mean(with_stacked, axis=0), np.mean(without_stacked, axis=0)
    with_stdevs, without_stdevs = np.std(with_stacked, axis=0), np.std(without_stacked, axis=0)

    # TODO: print errors, print vertical lines indicating the days more clearly, plot point cloud?

    plt.plot(with_means, '0.8', label="Jam occurrences with memory")
    plt.plot(without_means, '0.2', label="Jam occurrences without memory")
    pylab.legend(loc='upper left')
    plt.xlabel("Timestep")
    plt.xticks(np.arange(0, 300, 30))
    plt.ylabel("Average of total jams occurred per intersection (err or is it?)")
    plt.title("Occurence of jams with vs without memory (averaged over %i simulations)" % n_sims)
    plt.show()

if __name__ == '__main__':
    main()
