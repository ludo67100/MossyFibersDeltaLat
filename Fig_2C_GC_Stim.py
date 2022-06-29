# -*- coding: utf-8 -*-
"""
Created on Tue May 24 18:40:55 2022

@author: klab
"""

import matplotlib.pyplot as plt 
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams.update({'font.size': 7})
import pandas as pd 
import numpy as np
from scipy.optimize import curve_fit

granuleCellDeltaLatencies = pd.read_excel('D:/01_PAPERS/Binda_Spaeth_et_al/000_May_2022/TABLES/GC_ElecStim_DeltaLat.xlsx',
                                          header=0)['GC_Stim_DeltaLat (ms)'].values

plt.figure()
plt.xlabel('DeltaLat (ms)'); plt.ylabel('Normed Occurence')
plt.xlim(-10,10)

n, bins = np.histogram(granuleCellDeltaLatencies, bins=np.arange(0,6,0.225), density=True)

plt.bar(bins[:-1],n, facecolor='white',edgecolor='0.25',width=bins[1]-bins[0], label='Data')


# Let's create a function to model and create data
def func(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
  
# Generating clean data
x = bins[:-1]
y = n

  
  
# Executing curve_fit on noisy data
popt, pcov = curve_fit(func, x, y)
  
#popt returns the best fit values for parameters of the given model (func)
print (popt)
  
ym = func(x, popt[0], popt[1], popt[2])
plt.plot(x, ym, color='brown', linewidth=3, label='Gaussian Fit')


lowerDeltaLat = np.nanmean(granuleCellDeltaLatencies)-2*np.nanstd(granuleCellDeltaLatencies)
higherDeltaLat = np.nanmean(granuleCellDeltaLatencies)+2*np.nanstd(granuleCellDeltaLatencies)

plt.axvspan(xmin=lowerDeltaLat,xmax=higherDeltaLat, alpha=0.2)


