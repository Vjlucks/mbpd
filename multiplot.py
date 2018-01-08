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

x_0 = raw_input("Enter Starting x value: ")
x_l = raw_input("Enter final x value: ")
ext = raw_input("Are the files xy type or txt?")
ttl = raw_input("Enter the title: ")
yaxis = raw_input("Enter the y-axis title: ")
xaxis = raw_input("Enter the x-axis title: ")

if ext == "xy":
    delemeter = ''
else:
    delemeter = ','


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
    file_name = os.path.basename(file_path).replace('%s' % ext, '')
    return file_name


def read_target_files():
    """
        reads a directory and returns all the files matching a pattern
        :return: list
        """
    s = raw_input("File starting with:")
    return glob.glob("%s/%s*.%s" % (BASE_DIR,s, ext))


def get_subplots(count):
    """
    initializes the plot
    :return: None
    """
    f, sub_plots = plt.subplots(int(count), sharex=True, sharey=True)

    return sub_plots


def arrange_plots(sub_plot, file_path_list):
    """
    arranges the plot
    :return: None
    """
    
    for index, file_path in enumerate(file_path_list):
        selected_color = COLOR_SET[index]
        file_name = get_filename_from_file_path(file_path)
        np_object_from_text = np.genfromtxt(file_path, delimiter=delemeter, skip_header=2, skip_footer=0)
        t = np_object_from_text[:, 0]
        np_object_from_text = np_object_from_text[:, 1]
        sub_plot.plot(t, np_object_from_text, label=file_name, color= selected_color)
        sub_plot.legend(loc='upper right')
        plt.xlim(int(x_0), int(x_l))
        plt.title('%s' %ttl, fontsize = 20)
        plt.xlabel('%s' %xaxis, fontsize = 20)
        plt.ylabel('%s' %yaxis, fontsize = 20)
        plt.yticks([])
        sub_plot.grid()
        plt.savefig('XRDPlot.png', bbox_inches='tight')
        

def arrange_single_plots(file_path_list):
    """
    arranges the plot
    :return: None
    """
    i = 0
    for index, file_path in enumerate(file_path_list):
        selected_color = COLOR_SET[index]
        file_name = get_filename_from_file_path(file_path)
        np_object_from_text = np.genfromtxt(file_path, delimiter=delemeter, skip_header=2, skip_footer=0)
        t = np_object_from_text[:, 0]
        np_object_from_text = np_object_from_text[:, 1]
        np_object_from_text = [b+i for b in np_object_from_text]
        plt.plot(t, np_object_from_text, label=file_name, color=selected_color)
        plt.legend(loc=1)
        plt.xlim(int(x_0), int(x_l))
        plt.title('%s' %ttl, fontsize = 20)
        plt.xlabel('%s' %xaxis, fontsize = 20)
        plt.ylabel('%s' %yaxis, fontsize = 20)
        plt.yticks([])
        plt.grid(True)
        plt.savefig('XRDPlot.png', bbox_inches='tight')
        i += 10

def show_plot():
    """
    plots the plot
    :return: None
    """
    plt.show()


def main():
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

