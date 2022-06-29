# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:40:41 2021

@author: LS in klab
"""

#Fill as path the folder containing the data
mainDir = 'D:/01_PAPERS/Binda_Spaeth_et_al/000_May_2022/TABLES'

#Fill as path to save the plots and tables
saveDir = 'D:/01_PAPERS/Binda_Spaeth_et_al/000_May_2022/PLOTS'

#---------------------------------------------------------------------------------------------------
#------------------------The code below will generate the plots as shown in ------------------------
#------------------------------------------the paper------------------------------------------------
#---------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    files = ['{}/FluoViewDataSet_LatencyMeasuresCleaned.xlsx'.format(mainDir),
             '{}/MosaicDataSet_LatencyMeasuresCleaned.xlsx'.format(mainDir)]
    
    datasetLabels = ['Surface','Single']
    
    FFIBorders = [0.52, 3.48]
    
    alpha=0.75
    
    #Amout of I only in each dataset
    inhibitionOnlySingle = 4
    inhibitionOnlySurface = 10
    
    IOnly = [inhibitionOnlySurface,inhibitionOnlySingle]
    
    import pandas as pd 
    import matplotlib
    matplotlib.rcParams['pdf.fonttype'] = 42
    from matplotlib import pyplot as plt 
    import numpy as np
    from scipy import stats
    import electroPyy
    from scipy.optimize import curve_fit
    
    timeBins = np.arange(0,30,1)
    deltaBins = np.arange(-15,15, 1)
    weightBins = np.arange(-20, 40, 1)
    variables = ['Lat. Exc. (ms)','Lat. Inh. (ms)','Delta Lat. (ms)','EPSQ (pC)', 'IPSQ (pC)' ]
    bins = [timeBins,timeBins, deltaBins, weightBins, weightBins]
    
    deltaLatDist = []
    
    #FIGURE 1E---------------------------------------------------------------------------------------------
    #Plot surface vs single illumination
    print('------------------------FIGURE 1E--------------------------')
    datasetFig, datasetAx = plt.subplots(1,len(variables), figsize=(9,3), sharey = True)
    datasetFig.suptitle('Surface vs Single Illumination')
    
    #Compare Charges between surgace anf single
    excCharges, inhCharges = [], []
    excLatency, inhLatency = [], []
    deltaLatToCompare = []
    
    for file, datasetLabel in zip(files, datasetLabels): 
        
        print('-------{}-------'.format(datasetLabel))
        
        df = pd.read_excel(file, header=0)
        
        deltaLatDist.append(df['Delta Lat. (ms)'].values)
        
        for i in range(len(variables)): 
            
            print(variables[i])
            
            avg = df[variables[i]].mean()
            std = df[variables[i]].std()
            
            if variables[i] == 'EPSQ (pC)':
                excCharges.append(df[variables[i]].values)
                
            if variables[i] == 'IPSQ (pC)':
                inhCharges.append(df[variables[i]].values)
                
            if variables[i] == 'Lat. Exc. (ms)':
                excLatency.append(df[variables[i]].values)
                
            if variables[i] == 'Lat. Inh. (ms)':
                inhLatency.append(df[variables[i]].values)
                
            if variables[i] == 'Delta Lat. (ms)':
                deltaLatToCompare.append(df[variables[i]].values)
                
                
        
            print('Avg = {}'.format(avg))
            print('SD = {}'.format(std))
            print('min = {}'.format(df[variables[i]].min()))
            print('max = {}'.format(df[variables[i]].max()))
            print('n={}'.format(len(df[variables[i]].values)))
            print()
            
            datasetAx[i].hist(df[variables[i]], bins=bins[i],density=True,   label=datasetLabel, alpha=alpha)
            datasetAx[i].set_xlabel(variables[i])
            
            datasetAx[i].legend(loc='best')
            
            
            
    #Stats between Single and Surface
    #EPSQ
    print('Stat: Single vs Surface')
    print('EPSQ test')
    print(stats.shapiro(excCharges[0]))
    print(stats.shapiro(excCharges[1]))
    epsqTest = stats.ks_2samp(excCharges[0], excCharges[1])
    mwu = stats.mannwhitneyu(excCharges[0], excCharges[1])
    print(mwu)
    print(epsqTest)
    ttestind = stats.ttest_ind(excCharges[0], excCharges[1])
    print(ttestind)
    print()
    
    #IPSQ
    print('IPSQ test')
    print(stats.shapiro(inhCharges[0]))
    print(stats.shapiro(inhCharges[1]))
    ipsqTest = stats.ks_2samp(inhCharges[0], inhCharges[1])
    mwu = stats.mannwhitneyu(inhCharges[0], inhCharges[1])
    ttestind = stats.ttest_ind(inhCharges[0], inhCharges[1])
    print(ttestind)
    print(mwu)
    print(ipsqTest)
    print()
    
    #Exc Latency
    print('EPSC Latency')
    print(stats.shapiro(excLatency[0]))
    print(stats.shapiro(excLatency[1]))
    mwu = stats.mannwhitneyu(excLatency[0], excLatency[1])
    print(mwu)
    epscLatTest = stats.ks_2samp(excLatency[0], excLatency[1])
    print(epscLatTest)
    ttestind = stats.ttest_ind(excLatency[0], excLatency[1])
    print(ttestind)
    print()
    
    #Inh Latency
    print('IPSC Latency')
    print(stats.shapiro(inhLatency[0]))
    print(stats.shapiro(inhLatency[1]))
    mwu = stats.mannwhitneyu(inhLatency[0], inhLatency[1])
    print(mwu)
    ipscLatTest = stats.ks_2samp(inhLatency[0], inhLatency[1])
    print(ipscLatTest)
    ttestind = stats.ttest_ind(inhLatency[0], inhLatency[1])
    print(ttestind)
    print()
    
    #DeltaLat
    print('DeltaLat')
    print(stats.shapiro(deltaLatToCompare[0]))
    print(stats.shapiro(deltaLatToCompare[1]))
    mwu = stats.mannwhitneyu(deltaLatToCompare[0], deltaLatToCompare[1])
    print(mwu)
    DeltaLatTest = stats.ks_2samp(deltaLatToCompare[0], deltaLatToCompare[1])
    print(DeltaLatTest)
    ttestind = stats.ttest_ind(deltaLatToCompare[0], deltaLatToCompare[1])
    print(ttestind)
    print()
    
    
            
    plt.tight_layout()
            
            
    #FIGURE 2A/2B/2D-----------------------------------------------------------------------------------------
    #Focus on DeltaLat
    print('-----------------------FIGURE 2A/B/D-------------------------')
    deltaLatFig, deltaLatAx = plt.subplots(1,2, figsize=(5,3))
    
    for i in range(len(deltaLatDist)): 
        
        #Do hist
        deltaLatAx[i].set_title('{} illumination'.format(datasetLabels[i]))
        heights, bins, bars = deltaLatAx[i].hist(deltaLatDist[i], bins=deltaBins, density=True)
        deltaLatAx[i].set_xlabel('DeltaLat (ms)')
        
        
        #Gaussian function
        def func(x, a, x0, sigma):
            return a*np.exp(-(x-x0)**2/(2*sigma**2))
          
        #Trim data
        x = bins[:-1]
        y = heights
        
        #Curve fit
        popt, pcov = curve_fit(func, x, y)
          
        #return optimal fit parameters
        print (popt)
          
        ym = func(x, popt[0], popt[1], popt[2])
        deltaLatAx[i].plot(x, ym, color='blue', linewidth=2,linestyle='--', label='Gaussian Fit')
        
        for bar in bars:
            if FFIBorders[0] < bar.get_x() <= FFIBorders[1]:
                bar.set_facecolor('0.2')
            else:
                bar.set_facecolor('crimson')
                
        #Add custom legend
        from matplotlib.lines import Line2D
        custom_lines = [Line2D([0], [0], color='0.2', lw=4),
                        Line2D([0], [0], color='crimson', lw=4)]
    
        deltaLatAx[i].legend(custom_lines, ['FFI', 'Other'], loc='best')
              
    plt.tight_layout()
    
    
    #Propotions for PieCharts
    propPieFig, propPieAx = plt.subplots(1,2, figsize=(7,3))
    for i in range(len(deltaLatDist)):
    
        print('----{}----'.format(datasetLabels[i]))
        inhibitionFirst = [x for x in deltaLatDist[i] if x < 0]
        excitationFirst = [x for x in deltaLatDist[i] if x >= 0]
        
        trueFFI = [x for x in deltaLatDist[i] if FFIBorders[0] < x <= FFIBorders[1]]
        other = [x for x in deltaLatDist[i] if not FFIBorders[0] < x <= FFIBorders[1]]
        lessThanFFI = [x for x in deltaLatDist[i] if x < FFIBorders[0]]
        moreThanFFI = [x for x in deltaLatDist[i] if x > FFIBorders[1]]
        
        
        TotalExperiments = len(deltaLatDist[i])+IOnly[i]
        
        print('Total {} \n I before E {} \n E before I {} \n TrueFFI {} \n Other {} \n DeltaLAt < 0.52 {} \n DeltaLat > 3.48 {}\n I only {}'.format(TotalExperiments,
                                                                                                                                                    len(inhibitionFirst),
                                                                                                                                                    len(excitationFirst), 
                                                                                                                                                    len(trueFFI), 
                                                                                                                                                    len(other), 
                                                                                                                                                    len(lessThanFFI), 
                                                                                                                                                    len(moreThanFFI),
                                                                                                                                                    IOnly[i]))
        
        sizes = [len(lessThanFFI)/TotalExperiments*100,
                 len(trueFFI)/TotalExperiments*100,
                 len(moreThanFFI)/TotalExperiments*100, 
                 IOnly[i]/TotalExperiments*100]
        
        labels = ['DLat < {}'.format(FFIBorders[0]),
                  '{} < DLat < {}'.format(FFIBorders[0], FFIBorders[1]), 
                  'DLat > {}'.format(FFIBorders[1]),
                  'I only']
        
        piecolors = ['orange', '0.2', 'crimson', 'purple']
        
        propPieAx[i].pie(sizes, labels=labels,colors=piecolors, startangle=90, autopct='%1.1f%%')
        propPieAx[i].set_title('{} illumination'.format(datasetLabels[i]))
        
        
    #---------------------------FIGURE 3-------------------------------------------------
    print('--------------------FIGURE3--------------------')
    RegFig, RegAx = plt.subplots(3,2, figsize=(6,9), sharex=False, sharey=False)
    EIFig, EIAx = plt.subplots(1,2, figsize=(6,3), sharex=True, sharey=True)
    
    EI_distributions = []
    
    for file, datasetLabel, i in zip(files, datasetLabels, range(len(files))): 
        print('-------------{}----------'.format(datasetLabel))
    
        df = pd.read_excel(file, header=0)
        
        #Whole dataset-------------------------------------------------------------
        print()
        print('WHOLE DATA')
        EPSQs = abs(df['EPSQ (pC)'].values)
        IPSQs = abs(df['IPSQ (pC)'].values)
        
        px, nom, lpb, upb, r2, std, coeffs = electroPyy.core.Regression.LinReg(EPSQs,IPSQs,conf=0.95,printparams=True,plot=True, ax=RegAx[0,i]) 
        lineRegTest = stats.linregress(EPSQs, IPSQs)
        print(lineRegTest)
        print('n (EPSQ) = {} | n (IPSQ) = {}'.format(len(EPSQs),len(IPSQs)))
        
        #Group 1 only--------------------------------------------------------------
        print()
        print('Group 1: FFI')
        EPSQs = abs(df[df['group 0.52 to 3.48']==1]['EPSQ (pC)'].values)
        IPSQs = abs(df[df['group 0.52 to 3.48']==1]['IPSQ (pC)'].values)
        
        px, nom, lpb, upb, r2, std, coeffs = electroPyy.core.Regression.LinReg(EPSQs,IPSQs,conf=0.95,printparams=True,plot=True, ax=RegAx[1,i]) 
        lineRegTest = stats.linregress(EPSQs, IPSQs)
        print(lineRegTest)
        print('n (EPSQ) = {} | n (IPSQ) = {}'.format(len(EPSQs),len(IPSQs)))    
    
        #Group 2 only--------------------------------------------------------------
        print()
        print('Group 2: non FFI')
        EPSQs = abs(df[df['group 0.52 to 3.48']==2]['EPSQ (pC)'].values)
        IPSQs = abs(df[df['group 0.52 to 3.48']==2]['IPSQ (pC)'].values)
        
        px, nom, lpb, upb, r2, std, coeffs = electroPyy.core.Regression.LinReg(EPSQs,IPSQs,conf=0.95,printparams=True,plot=True, ax=RegAx[2,i]) 
        lineRegTest = stats.linregress(EPSQs, IPSQs)
        print(lineRegTest)
        print('n (EPSQ) = {} | n (IPSQ) = {}'.format(len(EPSQs),len(IPSQs)))   
        
        
        
        #E/I ratio-----------------------------------------------------------------
        
        print()
        print('E/I Ratio')
        EIratio = abs(df['EPSQ (pC)'].values)/abs(df['IPSQ (pC)'].values)
        
        EIAx[i].hist(EIratio, bins=np.arange(0,1,0.05))
        EIAx[i].set_title('{} illumination'.format(datasetLabel))
        EIAx[i].set_xlabel('E/I')
        
        print('Avg = {}'.format(np.nanmean(EIratio)))
        print('SD = {}'.format(np.nanstd(EIratio)))
        
        EI_distributions.append(EIratio)
        
    plt.tight_layout()
    RegFig.tight_layout()
        
    
    #Test EI Ratios 
    
    singleEInorm = stats.shapiro(EI_distributions[1])
    surfaceEInorm = stats.shapiro(EI_distributions[0])
    
    if singleEInorm[1] < 0.05 or surfaceEInorm[1] < 0.05:
        print('E/I Distributions are not following normal dist.')
        
        mwuEI = stats.mannwhitneyu(EI_distributions[1],EI_distributions[0])
        print(mwuEI)
        
    
    datasetFig.savefig('{}/SurfaceVSSingle_Variables.pdf'.format(saveDir))
    deltaLatFig.savefig('{}/DeltaLatPlot.pdf'.format(saveDir))
    propPieFig.savefig('{}/Piecharts.pdf'.format(saveDir))
    RegFig.savefig('{}/RegressionLines.pdf'.format(saveDir))
    EIFig.savefig('{}/EIRatio.pdf'.format(saveDir))
        
        
        
        
        
        
        
        