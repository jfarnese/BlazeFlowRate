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
        # removing erroneous values to properly plot FRR stats
        # self.df['Aqueous Flow Rate'][self.df['Aqueous Flow Rate']
        #                              < 5] = self.df['Aqueous Flow Rate'].mean()
        # # # removing erroneous values to properly plot FRR stats
        # self.df['Organic Flow Rate'][self.df['Organic Flow Rate']
        #                              < 5] = self.df['Organic Flow Rate'].mean()
        # self.df = self.df.rename({'Center Flow Rate': 'Aqueous Flow Rate', 'Right Flow Rate': 'Organic Flow Rate', 'OrgFlow_proto_': 'org_fr', 'ORGpressure': 'org_pressure'}, axis=1)    #rename column headers

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
# Derived Values
# =============================================================================
        # self.df['FRR'] = self.df['Aqueous Flow Rate']/self.df['Organic Flow Rate']
        # self.df['TFR'] = self.df['Aqueous Flow Rate'] + self.df['Organic Flow Rate']
        # self.df['FRR percent error'] = calc_percent_error(self.df['FRR'], self.df['FRR'].mean())
        # self.df['absolute FRR percent error'] = calc_absolute_percent_error(
        #     self.df['FRR'], self.df['FRR'].mean())

        # sos = signal.butter(2, 40, fs=1000, output='sos')
        # self.df['Aqeuousflowfiltered'] = signal.sosfilt(sos, self.df['Aqueous Flow Rate'])
        # self.df['Organicflowfiltered'] = signal.sosfilt(sos, self.df['Organic Flow Rate'])
        # self.df['FRRfiltered'] = self.df['Aqeuousflowfiltered']/self.df['Organicflowfiltered']
        # self.df['FRRfiltered percent error'] = calc_percent_error(
        #     self.df['FRRfiltered'], self.df['FRRfiltered'].mean())
        # self.df['absolute FRRfiltered percent error'] = calc_absolute_percent_error(
        #     self.df['FRRfiltered'], self.df['FRRfiltered'].mean())

        # self.df['AqueousPresfiltered'] = signal.sosfilt(sos, self.df['Aqueous Pressure'])
        # self.df['OrganicPresfiltered'] = signal.sosfilt(sos, self.df['Organic Pressure'])
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
        self.df['Filtered Center Flow Rate'][self.df['Center Flow Rate'] < 2 *
                                              d1_stat['Center Flow Rate']['std']] = self.df['Center Flow Rate'].mean()
        self.df['Filtered Center Flow Rate'][self.df['Filtered Center Flow Rate'] > 2 *
                                    d1_stat['Center Flow Rate']['std']] = self.df['Center Flow Rate'].mean()

    #     # repeat for the right flow rate
        self.df['Filtered Right Flow Rate'][self.df['Right Flow Rate'] < 2 *
                                          d1_stat['Right Flow Rate']['std']] = self.df['Right Flow Rate'].mean()
        self.df['Filtered Right Flow Rate'][self.df['Filtered Right Flow Rate'] > 2 *
                                d1_stat['Right Flow Rate']['std']] = self.df['Right Flow Rate'].mean()

# =============================================================================
# Path to folder with CSV files
# =============================================================================

user_dir = r'C:\Users\jgee\Danaher\PLL PNI Engineering - Documents\\'
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

    d1_df.hist(column='Filtered Center Flow Rate', color='orange', bins=60, ax=ax7, alpha=0.5, rwidth=0.9)
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

    d1_df.hist(column='Filtered Right Flow Rate', color='violet', bins=60, ax=ax8, alpha=0.5, rwidth=0.9)
    # d1_df.hist(column='FRRfiltered', color='cyan', bins=60, ax=ax5, alpha=0.8, rwidth=0.9)
    ax8.axvline(x=d1_stat['Filtered Right Flow Rate']['mean'], color='cyan', linestyle='--',
                alpha=1, label="\u03BC =" + str(round(d1_stat['Filtereed Right Flow Rate']['mean'], 4)))

    ax8.axvline(x=(d1_stat['Filtered Right Flow Rate']['mean'] + 2*d1_stat['Filtered Right Flow Rate']['std']), ymax=0.3, color='cyan', linestyle='--',
                alpha=1, label="\u03BC +" + "2\u03C3 = " + "\u03BC + " + str(round(2*d1_stat['Right Flow Rate']['std'], 4)))
    ax8.set_xlabel('Flow Rate (mL/min)')
    ax8.set_ylabel('Bin Size')
    ax8.set_title('Filtered Right Flow Rate')
    ax8.legend(loc='right')
    
    
# =============================================================================
#     # pressure AQ
# =============================================================================

    # # d1_df.plot('Time', 'Aqueous Pressure', color='magenta', ax=ax1, label='\u03BC = ' +
    # #            str(round(d1_stat['Aqueous Pressure']['mean'], 2)) + 'psi')
    # d1_df.plot('Time', 'AqueousPresfiltered', color='magenta', ax=ax1, label='\u03BC = ' +
    #            str(round(d1_stat['AqueousPresfiltered']['mean'], 2)) + 'psi')
    # ax1.set_xlabel('')
    # ax1.set_ylabel('Pressure (psi)')
    # ax1.legend(loc='right')
    # ax1.set_title('Aqueous')
    # ax1.set_xlim(fr_zoom)

# =============================================================================
#     # pressure ORG
# =============================================================================

    # # d1_df.plot('Time', 'Organic Pressure', color='magenta', ax=ax2, label='\u03BC = ' +
    # #            str(round(d1_stat['Organic Pressure']['mean'], 2)) + 'psi')
    # d1_df.plot('Time', 'OrganicPresfiltered', color='magenta', ax=ax2, label='\u03BC = ' +
    #            str(round(d1_stat['OrganicPresfiltered']['mean'], 2)) + 'psi')
    # ax2.set_xlabel('')
    # ax2.legend(loc='right')
    # ax2.set_title('Organic')
    # ax2.set_xlim(fr_zoom)
    
    
# =============================================================================
#     # FRR hist
# =============================================================================
    # # d1_df.hist(column='FRR', color='orange', bins=60, ax=ax5, alpha=0.5, rwidth=0.9)
    # d1_df.hist(column='FRRfiltered', color='cyan', bins=60, ax=ax5, alpha=0.8, rwidth=0.9)
    # ax5.axvline(x=d1_stat['FRRfiltered']['mean'], color='lime', linestyle='--',
    #             alpha=1, label="\u03BC =" + str(round(d1_stat['FRRfiltered']['mean'], 4)))
    # ax5.axvline(x=(d1_stat['FRRfiltered']['mean'] + 2*d1_stat['FRRfiltered']['std']), ymax=0.3, color='red', linestyle='--',
    #             alpha=1, label="\u03BC +" + "2\u03C3 = " + "\u03BC + " + str(round(2*d1_stat['FRRfiltered']['std'], 4)))
    # ax5.set_xlabel('FRR')
    # ax5.set_ylabel('Bin Size')
    # ax5.set_title('FRRfiltered')
    # ax5.legend(loc='right')

# =============================================================================
#     # Error hist
# =============================================================================
    # # d1_df.hist(column='absolute FRR percent error', color='orange',
    # #            alpha=0.5, bins=60, ax=ax6, rwidth=0.9)
    # d1_df.hist(column='absolute FRRfiltered percent error', color='cornflowerblue',
    #            alpha=1, bins=60, ax=ax6, rwidth=0.9)

    # ax6.axvline(x=d1_stat['absolute FRRfiltered percent error']['95%'], color='lime', linestyle='--',
    #             alpha=1, label="95th = " + str(round(d1_stat['absolute FRRfiltered percent error']['95%'], 3))+"%")
    # ax6.axvline(x=(d1_stat['absolute FRRfiltered percent error']['99%']), color='red', linestyle='--',
    #             alpha=1, label="99th = " + str(round(d1_stat['absolute FRRfiltered percent error']['99%'], 3))+"%")
    # ax6.set_xlabel('% Error')
    # ax6.set_xlim(0, 40)
    # ax6.legend(loc='right')
    # ax6.set_title('FRRfiltered Error from \u03BC')

# =============================================================================
#     # FRR plot
# =============================================================================
    # d1_df.plot('Time', 'FRRfiltered', color='cyan', ax=ax7, alpha=0.8, label='FRR')
    # ax7.axhline(y=d1_stat['FRRfiltered']['mean'], color='white', label='\u03BC', linestyle='--')
    # ax7.set_ylabel('FRRfiltered')
    # ax7.legend(loc='upper right')

# =============================================================================
# Pressure histograms
# =============================================================================

    # d1_df.hist(column='AqueousPresfiltered', color='orange', bins=60, ax=ax7, alpha=1, rwidth=0.9)
    # d1_df.hist(column='OrganicPresfiltered', color='cyan', bins=60, ax=ax7, alpha=0.5, rwidth=0.9)
    # ax7.axvline(x=d1_stat['AqueousPresfiltered']['mean'], color='orange', linestyle='--',
    #             alpha=1, label="Aq,\u03BC =" + str(round(d1_stat['AqueousPresfiltered']['mean'], 4)))
    # ax7.axvline(x=d1_stat['OrganicPresfiltered']['mean'], color='cyan', linestyle='--',
    #             alpha=1, label="Org,\u03BC =" + str(round(d1_stat['OrganicPresfiltered']['mean'], 4)))
    # # ax5.set_xlabel('Pressure')
    # ax7.set_ylabel('Bin Size')
    # ax7.set_title('Pressure')
    # ax7.legend(loc='right')

    # fig.savefig(save_path + csv_filelist[i][:-4] + '.png')

    print(csv_filelist[i])
    # print(d1_df['FRRfiltered'].mean())
    # print(d1_stat['absolute FRRfiltered percent error']['95%'])
    # print(d1_stat['absolute FRRfiltered percent error']['99%'])
    # print(2*d1_stat['FRRfiltered']['std'])
    # print(d1_df['Aqeuousflowfiltered'].mean())
    # print(d1_df['Organicflowfiltered'].mean())

    # print(d1_df['AqueousPresfiltered'].mean())
    # print(d1_df['OrganicPresfiltered'].mean())

    plt.show()
