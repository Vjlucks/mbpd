# -*- coding: utf-8 -*-

import matplotlib.pylab as plt
import numpy as np
import glob
import random
import sys
import os

COLOR_SET = [
    "k",
    "g",
    "r",
    "b",
    "c",
    "y"
]

BASE_DIR = ""
DELEMETER = ','
X_0 = 0
X_L = 0
EXT = ''
TTL = ''
Y_AXIS = ''
X_AXIS = ''


def set_variables():
    """
    sets default variables
    :return: None
    """
    global X_0
    global X_L
    global EXT
    global TTL
    global Y_AXIS
    global X_AXIS
    global DELEMETER

    X_0 = raw_input("Enter Starting x value: ")
    X_L = raw_input("Enter final x value: ")
    EXT = raw_input("Are the files xy type or txt?")
    TTL = raw_input("Enter the title: ")
    Y_AXIS = raw_input("Enter the y-axis title: ")
    X_AXIS = raw_input("Enter the x-axis title: ")

    if EXT == "xy":
        DELEMETER = ''


def initialize_plot():
    """
        initializes the plot
        :return: None
        """
    font = {
        'family': 'Times New Roman',
        'weight': 'bold',
        'size': 10
    }

    plt.rc('font', **font)
    plt.rc('xtick', labelsize=16)
    plt.rc('ytick', labelsize=16)

    plt.rcParams['axes.linewidth'] = 2


def get_filename_from_file_path(file_path):
    """
        returns file name if file_path includes it
        :param file_path: file path
        :return: file name, string
        """
    file_name = os.path.basename(file_path).replace('%s' % EXT, '')
    return file_name


def read_target_files():
    """
        reads a directory and returns all the files matching a pattern
        :return: list
        """
    return glob.glob("%s/*.%s" % (BASE_DIR, EXT))


def get_subplots(count):
    """
    initializes the plot
    :return: None
    """
    f, sub_plots = plt.subplots(int(count), sharex=True, sharey=True)
    f.text(0.5, 0.95, '%s' % (TTL), ha='center', va='center', fontsize=18)
    f.text(0.5, 0.02, '%s' % (X_AXIS), ha='center', va='center', fontsize=18)
    f.text(0.09, 0.5, '%s' % (Y_AXIS), ha='center', va='center', rotation='vertical', fontsize=18)

    return sub_plots


def arrange_plots(sub_plot, file_path):
    """
    arranges the plot
    :return: None
    """
    file_name = get_filename_from_file_path(file_path)
    np_object_from_text = np.genfromtxt(file_path, delimiter=DELEMETER, skip_header=2, skip_footer=0)
    t = np_object_from_text[:, 0]
    np_object_from_text = np_object_from_text[:, 1]
    sub_plot.plot(t, np_object_from_text, label=file_name, color=COLOR_SET[random.randint(0, len(COLOR_SET) - 1)])
    sub_plot.legend(loc='upper right')
    plt.xlim(int(X_0), int(X_L))

    plt.yticks([])
    sub_plot.grid()
    plt.savefig('XRDPlot.png', bbox_inches='tight')


def arrange_single_plots(file_path_list):
    """
    arranges the plot
    :return: None
    """
    for file_path in file_path_list:
        file_name = get_filename_from_file_path(file_path)
        np_object_from_text = np.genfromtxt(file_path, delimiter=DELEMETER, skip_header=2, skip_footer=0)
        t = np_object_from_text[:, 0]
        np_object_from_text = np_object_from_text[:, 1]
        plt.plot(t, np_object_from_text, label=file_name, color=COLOR_SET[random.randint(0, len(COLOR_SET) - 1)])
        plt.legend(loc='upper right')
        plt.xlim(int(X_0), int(X_L))
        plt.yticks([])
        plt.grid()
        plt.savefig('XRDPlot.png', bbox_inches='tight')


def show_plot():
    """
    plots the plot
    :return: None
    """
    plt.show()


def main():
    print "reading data from user\n"
    set_variables()

    print 'reading target directory=%s \n' % BASE_DIR
    file_list = read_target_files()
    plot_type = raw_input("Do you want stack plots or single?\n").strip()

    print 'initializing plot \n'
    initialize_plot()

    file_count = len(file_list)
    if file_count == 0:
        print "worthless zero subplots, exiting now!"
        sys.exit(1)

    if plot_type == 'stack':
        print 'generating subplots\n'
        sub_plots = get_subplots(file_count)

        print 'Arranging the plots one by one'
        for index, sub_plot in enumerate(sub_plots):
                print 'Working with file=%s \n' % file_list[index]
                arrange_plots(sub_plot, file_list[index])
    else:
        arrange_single_plots(file_list)

    print 'Enjoy the Plots.......!!'
    show_plot()

if __name__ == "__main__":
    main()

