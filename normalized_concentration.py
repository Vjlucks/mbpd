# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pylab as plt
import os
import sys
import glob
from openpyxl import Workbook

plt.rcParams['text.latex.preamble'] = [r'\boldmath']
FONT = {
    'family': 'Times New Roman',
    'weight': 'bold',
    'size': 11
}
plt.rc('font', **FONT)
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.rcParams['axes.linewidth'] = 2

TIME_INTERVAL = 30

BASE_DIR = ""
LOCAL_MAXIMUMS = []
MARKERS = [
    "*b-.",
    "or-",
    "xr-.",
    "sk-",
    "|k-.",
    "pb-.",
    "Dg-"]


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

    peakIllum = locmax[3:]
    peakIllum = np.max(peakIllum)/peakIllum
    Y = np.log(peakIllum)
    
    illutime = np.arange(90, 230, 30)
    illutime = illutime[:, np.newaxis]-90
    
    plt.plot(illutime, Y, 'ob-')
    a, _, _, _ = np.linalg.lstsq(illutime, Y)
    plt.plot(illutime, a*illutime)
    plt.axis([0, 125, 0, 2.5])
    plt.xticks(np.arange(0, 125, 30))
    plt.xlabel(r'Time, min', fontsize=20,fontweight='bold')
    plt.ylabel(r"$ln(C_0/C_t)$", fontsize = 20)
    plt.title("Linearized plots for Normalized Concentrations", fontsize=20, fontweight='bold')
    return locmax


def _finalise_plot():
    plt.rc('font', **FONT)
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['text.latex.preamble'] = [r'\boldmath']

    leg = plt.legend(loc=3, handlelength=0.7)
    if not leg:
        return
    for legobj in leg.legendHandles:
        legobj.set_linewidth(4.0)

    plt.axvline(x=30, linestyle='--', linewidth=2)
    plt.axvline(x=90.5, linestyle='--', linewidth=2)
    plt.axvspan(0, 90, facecolor='0.9', alpha=0.5)
    ax = plt.axes()
    ax.text(150, 0.95, 'Photo-degradation', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10})
    ax.text(45, 0.95, 'Equilibration', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 10})
    ax.text(16, 0.95, 'Ads', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.2, 'pad': 7})

    plt.axis([10, 200, 0, 1])
    plt.xticks(np.arange(0, 200, 30))
    plt.xlabel(r'Time, min', fontsize=20,fontweight='bold')
    plt.ylabel(r"$C_t/C_0$", fontsize = 20)
    plt.title("Normalized Concentrations Compared Over Time", fontsize=20, fontweight='bold')


def _plot(t):
    plt.figure()
    i = 0
    markers_count = len(MARKERS)
    for max_value in LOCAL_MAXIMUMS:
        for label, data in max_value.iteritems():
            plt.plot(t, data, MARKERS[i % markers_count], label=label, lw=2)
            i += 1


def _show_plot():
    plt.show()


def _dump_data_into_xl():
    """
    dumps data set into a xl sheet
    :return: None
    """
    wb = Workbook()
    ws = wb.create_sheet("Experiment Results")
    sheet_title_list_object = list()
    sheet_data_list_object = list()
    for item in LOCAL_MAXIMUMS:
        sheet_title_list_object.extend(item.keys())
        for i in item.values():
            data_item_list = list()
            for j in i:
                data_item_list.append("%s" % j)
            data_item_list = ','.join(data_item_list)
            sheet_data_list_object.append(data_item_list)
    sheet_data_list_object = ';'.join(sheet_data_list_object)
    sheet_data_list_object = np.matrix.getT(np.matrix(sheet_data_list_object)).tolist()
    sheet_data_list_object.insert(0, sheet_title_list_object)
    for data in sheet_data_list_object:
        ws.append(data)

    wb.save("mbpd.xlsx")


def _check_continue_dependency():
    """
    checks if the data is there, if not system exit.
    :return: None
    """
    if not LOCAL_MAXIMUMS:
        print 'ERROR: there is no data to work on, exiting, please re-check the BASE_DIR(current=%s)' % BASE_DIR
        sys.exit(1)


def main():
    print 'preparing data to plot'
    _prepare_data()

    print 'confirming before working on data'
    _check_continue_dependency()

    print 'dumping data into xl'
    _dump_data_into_xl()

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
