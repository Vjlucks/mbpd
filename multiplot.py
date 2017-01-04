# -*- coding: utf-8 -*-

import os
import operator
from matplotlib import pyplot
from pylab import *


font = dict(
    family='Times New Roman',
    weight='bold',
    size=13
)

matplotlib.rc('font', **font)
matplotlib.rc('xtick', labelsize=18)
matplotlib.rc('ytick', labelsize=18)
matplotlib.rcParams['axes.linewidth'] = 2

FILE_PATH = "/Users/mama/Downloads/Python/MBPD"


def _format_file_content(files):
    """
    removes lines those having no single comma(,)
    """
    for single_file in files:
        file_path = os.path.join(FILE_PATH, single_file)
        new_path = "%s.new" % file_path
        if os.path.exists(file_path):
            with open(file_path, 'rw') as original_file:
                with open(new_path, 'w') as new_file:
                    for line in original_file.readlines():
                        slitted_line = line.split(',')
                        if len(slitted_line) == 2:
                            new_file.write(line)
            os.rename(new_path, file_path)


def _get_data_in_ordered_list_to_draw(files):
    """
    does very minor comparison and returns a list of dict containing file name and peak value
    """
    ordered_dict_label = dict()
    ordered_dict_data = dict()
    for single_file in files:
        label = os.path.basename(single_file).replace('.txt', '')
        data = np.genfromtxt(single_file, delimiter=',', skip_header=2, skip_footer=0)
        ordered_dict_data[label] = data
        ordered_dict_label[label] = max(data[:, 1])
        print "peak value of %s is %s" % (label, ordered_dict_label[label])
    ordered_dict_label = sorted(ordered_dict_label.items(), key=operator.itemgetter(1))
    data_list = list()
    for label in ordered_dict_label:
        data_list.append({label[0]: ordered_dict_data[label[0]]})
    data_list.reverse()
    return data_list


def _get_text_files():
    """
    returns a list of .txt files located in <FILE_PATH>
    """
    return [os.path.join(FILE_PATH, f) for f in os.listdir(FILE_PATH) if str(f).endswith('.txt')]


def _update_legend():
    """
    updates legends
    """
    leg = pyplot.legend(loc="best", handlelength=0.7)
    for legend_object in leg.legendHandles:
        legend_object.set_linewidth(4.0)


def _plot(target_files):
    _format_file_content(target_files)
    prepared_data = _get_data_in_ordered_list_to_draw(target_files)
    for single_data in prepared_data:
        for label, data in single_data.iteritems():
            try:
                pyplot.plot(data[:, 0], data[:, 1], label=label, lw=2)
            except Exception, e:
                print "Couldn't plot data, %s, Label(%s)" % (str(e), label)
    _update_legend()
    pyplot.show()
    pyplot.xlim(550, 750)
    pyplot.ylim(0, 2)

    pyplot.xlabel('Wavelength, nm', fontsize=18, fontweight='bold')
    pyplot.ylabel('Absorbance, abs', fontsize=18, fontweight='bold')
    pyplot.title("$0.075g$ $ Ta_3N_5$ (Inhouse) Assisted $ 5$ $ ppm$ MBPD", fontsize=20, fontweight='bold')


def main():
    print 'generating documents from text file'
    target_files = _get_text_files()

    print 'plotting data...'
    _plot(target_files)
    print 'Done!'


if __name__ == "__main__":
    main()
