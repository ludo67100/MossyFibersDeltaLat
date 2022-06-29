# -*- coding: utf-8 -*-
"""
Created on Wed May 25 12:47:15 2022

@author: klab
"""

#Fill as path the folder containing the data
mainDir = 'D:/01_PAPERS/Binda_Spaeth_et_al/000_May_2022/TABLES'


#---------------------------------------------------------------------------------------------------
#------------------------The code below will generate the plots as shown in ------------------------
#------------------------------------------the paper------------------------------------------------
#---------------------------------------------------------------------------------------------------

if __name__ == '__main__': 

    import matplotlib.pyplot as plt 
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams.update({'font.size': 7})
    import numpy as np 
    import pandas as pd 
    import seaborn as sn 
    from scipy import stats
    
    dataFile = '{}/InhibitionOnlyAllDatasets.xlsx'.format(mainDir)
    
    df = pd.read_excel(dataFile)
    
    fig, ax = plt.subplots(1,3, sharey=True)
    ax[0].set_title('Surface vs single I only')
    sn.boxplot(y='IPSQ(pC)', x='DataSet', data=df, ax=ax[0])
    sn.swarmplot(y='IPSQ(pC)', x='DataSet', data=df, color='black', ax=ax[0])
    
    #Stats
    surfaceIonly = df.loc[df['DataSet']=='Surface']['IPSQ(pC)'].values
    singleIonly = df.loc[df['DataSet']=='Single']['IPSQ(pC)'].values
    
    mwu = stats.mannwhitneyu(surfaceIonly,singleIonly)
    print('IPSQ when I only; surface vs single')
    print(mwu)
    
    
    print()
    #Compare I in surface and single 
    #Single-------------------------------------------------------------------------------------------------------------------------
    print('Single: IPSQs in E+I vs IPSQs in I only')
    singleBothIPSQ = pd.read_excel('D:/01_PAPERS/Binda_Spaeth_et_al/000_May_2022/TABLES/MosaicDataSet_LatencyMeasuresCleaned.xlsx',
                                   header=0, index_col=0, sheet_name='E+I')['IPSQ (pC)'].values
    
    ax[1].boxplot([singleBothIPSQ,singleIonly], showmeans=True, showfliers=False)
    ax[1].scatter(np.linspace(0.8,1.2,len(singleBothIPSQ)),singleBothIPSQ)
    ax[1].scatter(np.linspace(1.8,2.2,len(singleIonly)),singleIonly)
    ax[1].set_title('Single Illumination')
    
    print('IPSQs (pC, E+I) mean+/-SD: {:.2f} +/- {:.2f}; n={}'.format(np.nanmean(singleBothIPSQ), np.nanstd(singleBothIPSQ),len(singleBothIPSQ)))
    print('IPSQs (pC, I Only) mean+/-SD: {:.2f} +/- {:.2f}; n={}'.format(np.nanmean(singleIonly), np.nanstd(singleIonly),len(singleIonly)))
    
    mwu=stats.mannwhitneyu(singleBothIPSQ,singleIonly)
    print(mwu)
    
    
    print()
    #Surface------------------------------------------------------------------------------------------------------------------------------
    surfaceBothIPSQ = pd.read_excel('D:/01_PAPERS/Binda_Spaeth_et_al/000_May_2022/TABLES/FluoViewDataSet_LatencyMeasuresCleaned.xlsx',
                                    header=0, index_col=0, sheet_name='E+I')['IPSQ (pC)'].values
    
    ax[2].boxplot([surfaceBothIPSQ,surfaceIonly], showmeans=True, showfliers=False)
    ax[2].scatter(np.linspace(0.8,1.2,len(surfaceBothIPSQ)),surfaceBothIPSQ)
    ax[2].scatter(np.linspace(1.8,2.2,len(surfaceIonly)),surfaceIonly)
    ax[2].set_title('Surface Illumination')
    
    print('IPSQs (pC, E+I) mean+/-SD: {:.2f} +/- {:.2f}; n={}'.format(np.nanmean(surfaceBothIPSQ), np.nanstd(surfaceBothIPSQ),len(surfaceBothIPSQ)))
    print('IPSQs (pC, I Only) mean+/-SD: {:.2f} +/- {:.2f}; n={}'.format(np.nanmean(surfaceIonly), np.nanstd(surfaceIonly),len(surfaceIonly)))
    
    mwu=stats.mannwhitneyu(surfaceBothIPSQ,surfaceIonly)
    print(mwu)
    
    fig.tight_layout()
    
    # parentDir = 'D:/01_PAPERS/Binda_Spaeth_et_al/Sorted/18-04-2019/Cell_3b/0'
    
    # lowFreq = 1
    # highFreq = 4000
    # channel = 0
    
    # #in Seconds
    # stimOnset = 0.5
    
    
    
    # reader = winraw('{}/{}'.format(parentDir, os.listdir(parentDir)[0]))
    # reader.parse_header()
    # sites = reader.header['nb_segment'][0]
    
    # fig, ax = plt.subplots(1,sites, sharex=True, sharey=True, figsize=(16,4))
    
    # for site in range(sites):
        
    #     tempTrace = []
    
    #     for file in os.listdir(parentDir): 
            
    #         reader = winraw('{}/{}'.format(parentDir, file))
    #         reader.parse_header()
            
    #         nb_sweeps =reader.header['nb_segment'][0]
    #         sampling = reader.get_signal_sampling_rate()
            
    #         channel_indexes = np.arange(0,len(reader.header['signal_channels']),1)
        
        
    #         raw_sigs = reader.get_analogsignal_chunk(block_index=0,seg_index=site,
    #                                                  i_start=0,i_stop=-1,
    #                                                  channel_indexes=channel_indexes)
            
    #         float_sigs = reader.rescale_signal_raw_to_float(raw_sigs,dtype='float64')
    #         #BANDPASS FILTER MAY ADD DEFLECTION JUST BEFORE STIM
    #         filtered_signal = filt.bandpass(float_sigs,axis=0, 
    #                                         freq_low=lowFreq,freq_high=highFreq,
    #                                         N=8, 
    #                                         filtertype='butter',
    #                                         sample_rate=sampling)[:,channel]
            
    #         tempTrace.append(filtered_signal)
        
    #         points = len(filtered_signal)
            
    #         time = np.arange(0,points,1)*1./sampling
    #         timeVector = time-stimOnset
            
    #         ax[site].plot(timeVector, filtered_signal, color='0.5', alpha=0.3)
    #         ax[site].set_xlim(-0.05, 0.1)
            
    #     #Average-------------------------------------
    #     avgSignal = np.nanmean(tempTrace, axis=0)
        
    #     ax[site].plot(timeVector, avgSignal, color='black')
        
    #     baseline = np.nanmean([y for (x,y) in zip(timeVector, avgSignal) if -0.02 <= x < 0.0])
    #     charge = trapz(y=np.array([y for (x,y) in zip(timeVector, avgSignal) if 0.0 <= x < 0.2])-baseline, dx=1./sampling)
        
    #     ax[site].set_title('Charge = {}pC'.format(round(charge, 2)))
        
        