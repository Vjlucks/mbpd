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

filename = 'Dec29_0.075Ta3N5MBPD'

FILE_PATH = "/Users/lekhnathkhanal/Downloads/Python/MBPD/*.txt"
DIR_LIST = sorted(glob.glob(FILE_PATH))
y = np.zeros(len(DIR_LIST))


def _prepare_data():
    for i, path in enumerate(DIR_LIST):
        x = np.genfromtxt(DIR_LIST[i], delimiter=',', skip_header=2, skip_footer=0)
        PeakAbs = np.max(x[:, 1])
        print "%s -> %s" % (os.path.basename(path).replace('.txt', ''), PeakAbs)
        print "------------------"
        y[i] = PeakAbs
    locMax = y/max(y)
    locMax = np.sort(locMax)[::-1]
    print"################################"
    print "And the Normalized Concentrations for %s placed in descending order are: %s" % (filename, locMax)

    c1 = [1.7, 0.8, 0.8, 0.8, 0.56, 0.23, 0.05, 0.02]
    c2 = [1.7, .98, 0.98, 0.98, .75, 0.52, 0.3, 0.23]

    t = [0, 30, 60,  90, 120, 150, 180, 210]
    return c1, c2, t


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
    plt.title("Normalized Concentrations Compared over time for \n %s" % filename, fontsize=20, fontweight='bold')


def _plot(c1, c2, t):
    plt.figure()
    plt.plot(t, c2, 'or-', t, c1, 'Db-', lw=2, label=True)


def _show_plot():
    plt.show()


def main():
    print 'preparing data to plot'
    c1, c2, t = _prepare_data()

    print 'plotting data'
    _plot(c1, c2, t)

    print 'finalising plot'
    _finalise_plot()

    print 'showing the result'
    _show_plot()

if __name__ == '__main__':
    main()
