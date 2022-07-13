# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 21:46:48 2022
more details here

Purpose
List expectations of file formats etc.

@author: jfarnese, Julia Gee


# =============================================================================
# Changes to make

change grid size back to 4x4
add plots for the new 
# =============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import io, signal
import pandas as pd
import seaborn as sns
import os

# Time,Channel A,Channel B,Center Flow Rate,Right Flow Rate


class LoadData:

    def __init__(self, fname):

        self.fname = fname
        self.df = pd.read_csv(parent_path + fname, skiprows=([1, 2]))  # skipped row with units

        self.df['Filtered Center Flow Rate'] = self.df['Center Flow Rate']
        self.df['Filtered Right Flow Rate'] = self.df['Right Flow Rate']

# =============================================================================
# Functions
# =============================================================================

        def calc_absolute_percent_error(data, target):
            pe = abs((data - target) / target * 100)
            return pe

        def calc_percent_error(data, target):
            pe = (data - target) / target * 100
            return pe


# =============================================================================
# Statistics
# =============================================================================
        # create stats dataframe
        self.stats = self.df.describe()

        # self.stats.loc[len(self.df.index)] = self.df.median()   #add the median to the last row for all columns
        self.stats.rename(index={'50%': "median"}, inplace=True)  # rename the last index as median

        # add the variance to the last row for all columns
        self.stats.loc[len(self.df.index)] = self.df.var()
        # rename the last index as variance
        self.stats.rename({self.stats.index[-1]: "variance"}, inplace=True)

        # add the variance to the last row for all columns
        self.stats.loc[len(self.df.index)] = self.df.skew()
        # rename the last index as variance
        self.stats.rename({self.stats.index[-1]: "skew"}, inplace=True)

        # add the percentile to the last row for all columns
        self.stats.loc[len(self.df.index)] = self.df.quantile(0.95)
        # rename the last index as percentile
        self.stats.rename({self.stats.index[-1]: "95%"}, inplace=True)

        # add the percentile to the last row for all columns
        self.stats.loc[len(self.df.index)] = self.df.quantile(0.98)
        # rename the last index as percentile
        self.stats.rename({self.stats.index[-1]: "98%"}, inplace=True)

        # add the percentile to the last row for all columns
        self.stats.loc[len(self.df.index)] = self.df.quantile(0.99)
        # rename the last index as percentile
        self.stats.rename({self.stats.index[-1]: "99%"}, inplace=True)


# =============================================================================
# Getting rid of spikes
# =============================================================================
# removing erroneous values to properly plot FRR stats

        self.df['Filtered Center Flow Rate'][self.df['Filtered Center Flow Rate'] < 2 *
                                             d1_stat['Center Flow Rate']['std']] = self.df['Center Flow Rate'].mean()
        self.df['Filtered Center Flow Rate'][self.df['Filtered Center Flow Rate'] > 2 *
                                             d1_stat['Center Flow Rate']['std']] = self.df['Center Flow Rate'].mean()

    #     # repeat for the right flow rate
        self.df['Filtered Right Flow Rate'][self.df['Filtered Right Flow Rate'] < 2 *
                                            d1_stat['Right Flow Rate']['std']] = self.df['Right Flow Rate'].mean()
        self.df['Filtered Right Flow Rate'][self.df['Filtered Right Flow Rate'] > 2 *
                                            d1_stat['Right Flow Rate']['std']] = self.df['Right Flow Rate'].mean()

# =============================================================================
# Path to folder with CSV files
# =============================================================================


user_dir = r'C:\Users\jfarnese\Danaher\PLL PNI Engineering - Documents\\'
folder = r'\02.0 Projects\Blaze Project\2.0 Testing\ENG-000673 Blaze Testing\Blaze Testing - July 2022\Data Analysis in Python\CSV Files\\'
plot_folder = r'02.0 Projects\Blaze Project\2.0 Testing\ENG-000673 Blaze Testing\Blaze Testing - July 2022\Data Analysis in Python\Statistic Plots\\'
parent_path = user_dir + folder + '\\'
save_path = user_dir + plot_folder

csv_filelist = []
with os.scandir(parent_path) as f2:
    for entry in f2:
        if entry.name.endswith(".csv") and entry.is_file():
            csv_filelist.append(entry.name)


file = []
file_df = []
file_stats = []
for idx, val in enumerate(csv_filelist):
    file.append(LoadData(csv_filelist[idx]))
    file_df.append(file[idx].df)
    file_stats.append(file[idx].stats)

plt.style.use('seaborn-darkgrid')
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey


for i, val in enumerate(csv_filelist):

    d1 = LoadData(csv_filelist[i])
    d1_df = d1.df.round(decimals=6)
    d1_stat = d1.stats.round(6)

    fig = plt.figure(figsize=(18, 12), tight_layout=True)
    plt.rcParams.update({'font.size': 18})
    plt.suptitle(csv_filelist[i])
    gridsize = [4, 4]

    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2)
    ax2 = plt.subplot2grid(gridsize, (0, 2), colspan=2)
    ax3 = plt.subplot2grid(gridsize, (1, 0), colspan=2)
    ax4 = plt.subplot2grid(gridsize, (1, 2), colspan=2)
    ax5 = plt.subplot2grid(gridsize, (2, 0), colspan=2)
    ax6 = plt.subplot2grid(gridsize, (2, 2), colspan=2)
    ax7 = plt.subplot2grid(gridsize, (3, 0), colspan=2)
    ax8 = plt.subplot2grid(gridsize, (3, 2), colspan=2)

    ax1.grid(color='#2A3459')  # grid colour
    ax2.grid(color='#2A3459')
    ax3.grid(color='#2A3459')
    ax4.grid(color='#2A3459')
    ax5.grid(color='#2A3459')
    ax6.grid(color='#2A3459')
    ax7.grid(color='#2A3459')
    ax8.grid(color='#2A3459')

    fr_zoom = [65, 70]  # set ax.set_xlim(range) for flow rate and pressure graphs

# =============================================================================
#     # Flow rate Center Flow Rate
# =============================================================================

    # d1_df.plot('Time', 'Aqueous Flow Rate', color='lime', ax=ax3, alpha=0.5,
    #            label='\u03BC = ' + str(round(d1_stat['Aqueous Flow Rate']['mean'], 2)) + ' mL/min')

    d1_df.plot('Time', 'Center Flow Rate', color='lime', ax=ax1, alpha=1,
               label='\u03BC = ' + str(round(d1_stat['Center Flow Rate']['mean'], 2)) + ' mL/min')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Flow Rate (mL/min)')
    ax1.set_title('Center Flow Rate')
    ax1.legend(loc='right')
    # ax3.set_xlim(fr_zoom)
    # ax3.set_ylim([500, 700])

# =============================================================================
#     # Flow rate Right Flow Rate
# =============================================================================

    # d1_df.plot('Time', 'Organic Flow Rate', color='lime', ax=ax4, alpha=0.5,
    #            label='\u03BC = ' + str(round(d1_stat['Organic Flow Rate']['mean'], 2)) + ' mL/min')

    d1_df.plot('Time', 'Right Flow Rate', color='violet', ax=ax2, alpha=1,
               label='\u03BC = ' + str(round(d1_stat['Right Flow Rate']['mean'], 2)) + ' mL/min')
    ax2.set_xlabel('Time (s)')
    ax2.set_title('Right Flow Rate')
    ax2.legend(loc='right')
    # ax4.set_xlim(fr_zoom)
    # ax4.set_ylim([170, 300])

# =============================================================================
#     # Center Flow Rate Histogram
# =============================================================================

    d1_df.hist(column='Center Flow Rate', color='Lime', bins=60, ax=ax3, alpha=0.5, rwidth=0.9)
    # d1_df.hist(column='FRRfiltered', color='cyan', bins=60, ax=ax5, alpha=0.8, rwidth=0.9)
    ax3.axvline(x=d1_stat['Center Flow Rate']['mean'], color='lime', linestyle='--',
                alpha=1, label="\u03BC =" + str(round(d1_stat['Center Flow Rate']['mean'], 4)))

    ax3.axvline(x=(d1_stat['Center Flow Rate']['mean'] + 2*d1_stat['Center Flow Rate']['std']), ymax=0.3, color='red', linestyle='--',
                alpha=1, label="\u03BC +" + "2\u03C3 = " + "\u03BC + " + str(round(2*d1_stat['Center Flow Rate']['std'], 4)))
    ax3.set_xlabel('Flow Rate (mL/min)')
    ax3.set_ylabel('Bin Size')
    ax3.set_title('Center Flow Rate')
    ax3.legend(loc='right')

# =============================================================================
#     # Right Flow Rate Histogram
# =============================================================================

    d1_df.hist(column='Right Flow Rate', color='violet', bins=60, ax=ax4, alpha=0.5, rwidth=0.9)
    # d1_df.hist(column='FRRfiltered', color='cyan', bins=60, ax=ax5, alpha=0.8, rwidth=0.9)
    ax4.axvline(x=d1_stat['Right Flow Rate']['mean'], color='lime', linestyle='--',
                alpha=1, label="\u03BC =" + str(round(d1_stat['Right Flow Rate']['mean'], 4)))

    ax4.axvline(x=(d1_stat['Right Flow Rate']['mean'] + 2*d1_stat['Right Flow Rate']['std']), ymax=0.3, color='red', linestyle='--',
                alpha=1, label="\u03BC +" + "2\u03C3 = " + "\u03BC + " + str(round(2*d1_stat['Right Flow Rate']['std'], 4)))
    ax4.set_xlabel('Flow Rate (mL/min)')
    ax4.set_ylabel('Bin Size')
    ax4.set_title('Right Flow Rate')
    ax4.legend(loc='right')

 # =============================================================================
 #     # Filtered Flow rate Center Flow Rate
 # =============================================================================

    # d1_df.plot('Time', 'Aqueous Flow Rate', color='lime', ax=ax3, alpha=0.5,
    #            label='\u03BC = ' + str(round(d1_stat['Aqueous Flow Rate']['mean'], 2)) + ' mL/min')

    d1_df.plot('Time', 'Filtered Center Flow Rate', color='orange', ax=ax5, alpha=1,
               label='\u03BC = ' + str(round(d1_stat['Filtered Center Flow Rate']['mean'], 2)) + ' mL/min')
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Flow Rate (mL/min)')
    ax5.set_title('Filtered Center Flow Rate')
    ax5.legend(loc='right')
    # ax3.set_xlim(fr_zoom)
    # ax3.set_ylim([500, 700])

 # =============================================================================
 #     # Filtered Flow rate Right Flow Rate
 # =============================================================================

    # d1_df.plot('Time', 'Organic Flow Rate', color='lime', ax=ax4, alpha=0.5,
    #            label='\u03BC = ' + str(round(d1_stat['Organic Flow Rate']['mean'], 2)) + ' mL/min')

    d1_df.plot('Time', 'Filtered Right Flow Rate', color='cyan', ax=ax6, alpha=1,
               label='\u03BC = ' + str(round(d1_stat['Filtered Right Flow Rate']['mean'], 2)) + ' mL/min')
    ax6.set_xlabel('Time (s)')
    ax6.set_title('Filtered Right Flow Rate')
    ax6.legend(loc='right')
    # ax4.set_xlim(fr_zoom)
    # ax4.set_ylim([170, 300])


# =============================================================================
#     # Filtered Center Flow Rate Histogram
# =============================================================================

    d1_df.hist(column='Filtered Center Flow Rate', color='orange',
               bins=60, ax=ax7, alpha=0.5, rwidth=0.9)
    # d1_df.hist(column='FRRfiltered', color='cyan', bins=60, ax=ax5, alpha=0.8, rwidth=0.9)
    ax7.axvline(x=d1_stat['Filtered Center Flow Rate']['mean'], color='orange', linestyle='--',
                alpha=1, label="\u03BC =" + str(round(d1_stat['Filtered Center Flow Rate']['mean'], 4)))

    ax7.axvline(x=(d1_stat['Filtered Center Flow Rate']['mean'] + 2*d1_stat['Filtered Center Flow Rate']['std']), ymax=0.3, color='red', linestyle='--',
                alpha=1, label="\u03BC +" + "2\u03C3 = " + "\u03BC + " + str(round(2*d1_stat['Filtered Center Flow Rate']['std'], 4)))
    ax7.set_xlabel('Flow Rate (mL/min)')
    ax7.set_ylabel('Bin Size')
    ax7.set_title('Filtered Center Flow Rate')
    ax7.legend(loc='right')

# =============================================================================
#     # Filtered Right Flow Rate Histogram
# =============================================================================

    d1_df.hist(column='Filtered Right Flow Rate', color='violet',
               bins=60, ax=ax8, alpha=0.5, rwidth=0.9)
    # d1_df.hist(column='FRRfiltered', color='cyan', bins=60, ax=ax5, alpha=0.8, rwidth=0.9)
    ax8.axvline(x=d1_stat['Filtered Right Flow Rate']['mean'], color='cyan', linestyle='--',
                alpha=1, label="\u03BC =" + str(round(d1_stat['Filtereed Right Flow Rate']['mean'], 4)))

    ax8.axvline(x=(d1_stat['Filtered Right Flow Rate']['mean'] + 2*d1_stat['Filtered Right Flow Rate']['std']), ymax=0.3, color='cyan', linestyle='--',
                alpha=1, label="\u03BC +" + "2\u03C3 = " + "\u03BC + " + str(round(2*d1_stat['Right Flow Rate']['std'], 4)))
    ax8.set_xlabel('Flow Rate (mL/min)')
    ax8.set_ylabel('Bin Size')
    ax8.set_title('Filtered Right Flow Rate')
    ax8.legend(loc='right')

    # fig.savefig(save_path + csv_filelist[i][:-4] + '.png')

    print(csv_filelist[i])

    plt.show()
