# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os
import glob

FONT = {
    'family': 'Times New Roman',
    'weight': 'bold',
    'size': 13
}
TIME_INTERVAL = 30

BASE_DIR = ""
LOCAL_MAXIMUMS = []
MARKERS = [
    "Db-",
    "or-",
    "pk-"
]


def _construct_time_intervals():
    count = 0
    if LOCAL_MAXIMUMS:
        count = len(LOCAL_MAXIMUMS[0].values()[0])
    time_interval = np.zeros(count)
    increase_on = 0
    for i in xrange(count):
        time_interval[i] = increase_on
        increase_on += TIME_INTERVAL
    return time_interval


def _prepare_data():
    if os.path.exists(BASE_DIR):
        local_dirs = os.listdir(BASE_DIR)
        for local_dir in local_dirs:
            target_dir = os.path.join(BASE_DIR, local_dir)
            if os.path.isdir(target_dir) and os.path.exists(target_dir):
                local_max = _get_one_maximum(target_dir)
                LOCAL_MAXIMUMS.append({local_dir: local_max})


def _get_one_maximum(single_dir_name):
    target_files = glob.glob("%s/*.txt" % single_dir_name)
    y = np.zeros(len(target_files))
    for i, path in enumerate(target_files):
        x = np.genfromtxt(path, delimiter=',', skip_header=2, skip_footer=0)
        peakabs = np.max(x[:, 1])
        y[i] = peakabs
    locmax = y/max(y)
    locmax = np.sort(locmax)[::-1]

    return locmax


def _finalise_plot():
    plt.rc('font', **FONT)
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    plt.rcParams['axes.linewidth'] = 2

    leg = plt.legend(loc="best", handlelength=0.7)
    for legobj in leg.legendHandles:
        legobj.set_linewidth(4.0)

    plt.axvline(x=90.5, linestyle='--', linewidth=2)
    plt.axvspan(0, 90, facecolor='0.9', alpha=0.5)
    ax = plt.axes()
    ax.text(100, 1.8, 'Photo-degradation', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10})
    ax.text(45, 1.8, 'Equilibration', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10})
    ax.text(10, 1.8, 'Ads', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10})

    plt.annotate('Light On', xy=(90, 0), xytext=(45, 0.3),
                arrowprops=dict(facecolor='black', shrink=0.1))

    plt.axis([10, 200, 0, 2])
    plt.xticks(np.arange(0, 200, 30))
    plt.xlabel('Time, min', fontsize=18, fontweight='bold')
    plt.ylabel('Normalized Concentration, $C_t/C_0$', fontsize=18, fontweight='bold')
    plt.title("Normalized Concentrations Compared over time for \n Dec29_0.075Ta3N5MBPD", fontsize=20, fontweight='bold')


def _plot(t):
    plt.figure()
    i = 0
    markers_count = len(MARKERS)
    for max_value in LOCAL_MAXIMUMS:
        for label, data in max_value.iteritems():
            plt.plot(t, data, MARKERS[i % markers_count], label=label, lw=2)


def _show_plot():
    plt.show()


def main():
    print 'preparing data to plot'
    _prepare_data()

    print 'constructing time intervals'
    t = _construct_time_intervals()
    print 'plotting data'
    _plot(t)

    print 'finalising plot'
    _finalise_plot()

    print 'showing the result'
    _show_plot()

if __name__ == '__main__':
    main()
