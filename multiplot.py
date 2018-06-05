# -*- coding: utf-8 -*-

import matplotlib.pylab as plt
import numpy as np
import glob
import sys
import os
plt.style.use(u'bmh')
COLOR_SET = [
    "r",
    "g",
    "k",
    "b",
    "k",
    "g"
]

BASE_DIR = ""

X_0 = 10
X_L = 90
EXTENSION = 'xy'
TITLE = 'Title'
Y_AXIS = 'Y-axis'
X_AXIS = 'X-axis'
DELIMITER = ''
FILE_FILTER = ''


def read_set_parameters():
    """
    expects different values from user and sets them to respective variables
    :return: None
    """
    global X_0, X_L, EXTENSION, TITLE, Y_AXIS, X_AXIS, DELIMITER, FILE_FILTER
    FILE_FILTER = raw_input("Enter file filter(files starting with): ") or FILE_FILTER

    print "if you wish to use the default values, type nothing!"

    X_0 = raw_input("Enter Starting x value: ") or X_0
    X_L = raw_input("Enter final x value: ") or X_L
    EXTENSION = raw_input("Are the files xy type or txt?") or EXTENSION
    TITLE = raw_input("Enter the title: ") or TITLE
    Y_AXIS = raw_input("Enter the y-axis title: ") or Y_AXIS
    X_AXIS = raw_input("Enter the x-axis title: ") or X_AXIS

    if EXTENSION is not "xy":
        DELIMITER = ','


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
    plt.title('%s' % TITLE, fontsize=20)
    plt.xlim(int(X_0), int(X_L))
    plt.xlabel('%s' % X_AXIS, fontsize=20)
    plt.ylabel('%s' % Y_AXIS, fontsize=20)
    plt.yticks([])


def get_filename_from_file_path(file_path):
    """
        returns file name if file_path includes it
        :param file_path: file path
        :return: file name, string
        """
    file_name = os.path.basename(file_path).replace(EXTENSION, '')
    return file_name


def read_target_files():
    """
        reads a directory and returns all the files matching a pattern
        :return: list
        """
    return glob.glob("%s/%s*.%s" % (BASE_DIR, FILE_FILTER, EXTENSION))


def get_subplots(count):
    """
    initializes the plot
    :return: None
    """
    f, sub_plots = plt.subplots(int(count), sharex=True, sharey=True)

    return sub_plots


def arrange_plots(sub_plot, file_path_list, index):
    """
    arranges the plot
    :return: None
    """
    for file_path in file_path_list:
        selected_color = COLOR_SET[len(COLOR_SET) % index]
        file_name = get_filename_from_file_path(file_path)
        np_object_from_text = np.genfromtxt(file_path, delimiter=DELIMITER, skip_header=2, skip_footer=0)
        t = np_object_from_text[:, 0]
        np_object_from_text = np_object_from_text[:, 1]
        sub_plot.plot(t, np_object_from_text, label=file_name, color=selected_color)
        sub_plot.legend(loc='upper right')
        sub_plot.grid(True)


def arrange_single_plots(file_path_list):
    """
    arranges the plot
    :return: None
    """
    i = 0
    for index, file_path in enumerate(file_path_list):
        selected_color = COLOR_SET[len(COLOR_SET) % (index + 1)]
        file_name = get_filename_from_file_path(file_path)
        np_object_from_text = np.genfromtxt(file_path, delimiter=DELIMITER, skip_header=2, skip_footer=0)
        t = np_object_from_text[:, 0]
        np_object_from_text = np_object_from_text[:, 1]
        np_object_from_text = [b+i for b in np_object_from_text]
        plt.plot(t, np_object_from_text, label=file_name, color=selected_color)
        plt.legend(loc=1)
        plt.grid(True)
        i += 10


def show_plot():
    """
    plots the plot, writes the output to a .png file too
    :return: None
    """
    plt.savefig('XRDPlot.png', bbox_inches='tight')
    plt.show()


def main():
    print 'reading and setting parameters from user'
    read_set_parameters()

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
                arrange_plots(sub_plot, [file_list[index]], index+1)
    else:
        arrange_single_plots(file_list)

    print 'Showing the plots'
    show_plot()


if __name__ == "__main__":
    main()

