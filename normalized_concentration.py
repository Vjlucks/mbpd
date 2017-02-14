# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pylab as plt
import os
import glob
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
#from scipy import stats


plt.rcParams['text.latex.preamble'] = [r'\boldmath']
#plt.rc('font', family='serif', serif='cm10')
#plt.rc('text', usetex=True)
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

BASE_DIR = "C:\Users\Laxmi Khanal\Desktop\Python\MBPD\Experiments"
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
    print locmax
    f =[]
    for i in locmax:
        f.append(i)
    rows = [
        target_files, ["C0/C0", 'C1/C0', 'C2/C0', 'C3/C0', 'C4/C0', 'C5/C0'],
        f
    ]
    
    for row in rows:
        ws.append(row)
    # Save the file
    wb.save("mbpd.xlsx")
    #%%
    peakIllum = locmax[3 :]
    peakIllum = np.max(peakIllum)/peakIllum
    Y = np.log(peakIllum)
    
    #print 'log(C0/Ct) is:%s' %(Y)
    IlluTime = np.arange(90, 230, 30)
    IlluTime = IlluTime[:,np.newaxis]-90
    
    plt.plot(IlluTime, Y, 'ob-')
    a, _, _, _ = np.linalg.lstsq(IlluTime, Y)
    #slope, intercept, r_value, p_value, std_err = stats.linregress(IlluTime,Y)
    #line = slope*(IlluTime-90)+intercept
    #print 'R-Squared value: %s' %(r_value)
    plt.plot(IlluTime, a*IlluTime)
    plt.axis([0, 125, 0,2.5 ])
    plt.xticks(np.arange(0, 125, 30))
    plt.xlabel(r'Time, min', fontsize=20,fontweight='bold')
    plt.ylabel(r"$ln(C_0/C_t)$", fontsize = 20)
    plt.title("Linearized plots for Normalized Concentrations", fontsize=20, fontweight='bold')
    #%%
    
    return locmax

    

    


def _finalise_plot():
    plt.rc('font', **FONT)
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['text.latex.preamble'] = [r'\boldmath']

    leg = plt.legend(loc=3, handlelength=0.7)
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

    #plt.annotate('Light On', xy=(90, 0), xytext=(45, 0.3),
    #            arrowprops=dict(facecolor='black', shrink=0.1))

    plt.axis([10, 200, 0, 1])
    plt.xticks(np.arange(0, 200, 30))
    plt.xlabel(r'Time, min', fontsize=20,fontweight='bold')
    plt.ylabel(r"$C_t/C_0$", fontsize = 20)
    plt.title("Normalized Concentrations Compared over Time", fontsize=20, fontweight='bold')


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
"""
#%%
from scipy import stats
import numpy as np
x = np.random.random(10)
y = np.random.random(10)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# To get coefficient of determination (r_squared)


print "r-squared:", r_value**2

#%%
"""