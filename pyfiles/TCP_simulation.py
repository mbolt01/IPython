# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:12:28 2016

@author: mb22
"""

#%%

#from TCP import *
import TCP
import matplotlib.pyplot as plt
import importlib
importlib.reload(TCP)

#%%

## array of doses - sepcify automatically based on list of SDs
## ALL will have to be saved in a single numpy array (multidimensional?)
size=1000
scales = np.arange(0.2,3.1,0.2) # specifies the differnt dose shifts for the linacs

print(scales)

all_doses = np.array([]) # start with empty array

## create array of the different doses. Each SD stored on different row.
for scale in scales:
    doses = np.random.normal(loc=0,scale=scale, size=size)
    all_doses = np.append(all_doses,doses) ## append resutls to array

## reshape np-array so that its on different rows
all_doses = np.reshape(all_doses,(-1,size)) # -1 menas only need to specify size in 1 direction

for i in range(len(scales)):
    plt.hist(all_doses[i], bins=50, alpha=0.5, histtype='step')

#%% 

## ***** Updated to include more dose_shift values contained in a single numpy array

## run single TCP calc with specified input values
## use this to loop through number of different dise shifts with other parameters fixed.
## this can build up a UK wide TCP variation and compare different variaitons in dose allowed

## random normal distribution of linac outputs

#outputs = [-2,-1,0,1,2] # specify a list of doses (which could be from different linacs)

#all_outputs = [doses1,doses2,doses3,doses4]
all_outputs = all_doses

sd_use = [0.5,1.0,1.5,2.0,2.5,3.0] # test a number of different sds
#outputs = doses3

for s in sd_use:
    print(sd_use)
    j=1
    for outputs in all_outputs:
        
        output_TCPs = []
        #pathname = r'C:\Users\mb22\OneDrive\PhD\Quasar Shared'
        #pathname2 = """\Modelling\IPython\OPs\"""
        
        fname = str(r'C:\Users\mb22\OneDrive\PhD\Quasar Shared\Modelling\IPython\TCP_variations_with_OP\all_TCP_doses_sd2-'+str(s))
        savename = fname + '\\' + 'all_TCP_doses_' + str(scales[j-1])
        print(savename)
        tot_len = len(outputs)
        i=1
        print('')
        print(str(j) + '/' + str(len(all_outputs)))
        for dose in outputs:
            perc_complete = i/tot_len *100    
            
            print('\r'+ str(round(perc_complete,1)) + '%', end="")
            #print('\r' + "Fitting N0: 100% complete")
            TCP_results = completeTCPcalc(n=2000,
                                          alphabeta_use=3,
                                          alphabeta_sd_use=0.5,
                                          d=2,
                                          d_shift=dose,
                                          d_sd=s,
                                          d_trend=0,
                                          n0=None,
                                          max_d=100,
                                          dose_of_interest=74)
            i=i+1
        
            output_TCPs.append(TCP_results[12]) #[10] is the TCP at dose_interest, [12] is TCP_pop
        j=j+1
        #np.savetxt(savename + '.txt', output_TCPs)
        np.save(savename + '.npy', output_TCPs)
    print('')
    #print(output_TCPs)
print('completed')


#%%

## array of doses - specified manually
size=1000

doses1 = np.random.normal(loc=0,scale=0.634118, size=size)
doses2 = np.random.normal(loc=0,scale=0.5, size=size)
doses3 = np.random.normal(loc=0,scale=0.25, size=size)
doses4 = np.random.normal(loc=0,scale=1.0, size=size)
plt.hist(doses1, bins=60, alpha=0.5, histtype='step')
plt.hist(doses2, bins=60, alpha=0.5, histtype='step')
plt.hist(doses3, bins=60, alpha=0.5, histtype='step')
plt.hist(doses4, bins=60, alpha=0.5, histtype='step')
plt.xlim(-3,3)

#%% 

## run single TCP calc with specified input values
## use this to loop through number of different dise shifts with other parameters fixed.
## this can build up a UK wide TCP variation and compare different variaitons in dose allowed

## random normal distribution of linac outputs

#outputs = [-2,-1,0,1,2] # specify a list of doses (which could be from different linacs)

all_outputs = [doses1,doses2,doses3,doses4]
#outputs = doses3
j=1
for outputs in all_outputs:
    
    output_TCPs = []
    #pathname = r'C:\Users\mb22\OneDrive\PhD\Quasar Shared'
    #pathname2 = """\Modelling\IPython\OPs\"""
    
    fname = str(r'C:\Users\mb22\OneDrive\PhD\Quasar Shared\Modelling\IPython\OPs')
    savename = fname + '\\' + 'all_TCP_doses' + str(j)
    tot_len = len(outputs)
    i=1
    print('')
    print(str(j) + '/' + str(len(all_outputs)))
    for dose in outputs:
        perc_complete = i/tot_len *100    
        
        print('\r'+ str(round(perc_complete,1)) + '%', end="")
        #print('\r' + "Fitting N0: 100% complete")
        TCP_results = completeTCPcalc(n=2000,
                                      alphabeta_use=3,
                                      alphabeta_sd_use=0.5,
                                      d=2,
                                      d_shift=dose,
                                      d_sd=0.5,
                                      d_trend=0,
                                      n0=170,
                                      max_d=100,
                                      dose_of_interest=74)
        i=i+1
    
        output_TCPs.append(TCP_results[12]) #[10] is the TCP at dose_interest, [12] is TCP_pop
    j=j+1
    #np.savetxt(savename + '.txt', output_TCPs)
    np.save(savename + '.npy', output_TCPs)
print('')
#print(output_TCPs)
print('completed')

#%%

plt.plot(output_TCPs)


#%%

## create single TCP plot to use as a 'standard' for visual comparison
## use doses1 as hte doses to use as this is the collected data.

## can simulate missed fractions

## ideally would create a funciton to convert doses stored in a file into a list
## this could potentially deal with anumber of different patients with doses in different rows.
## the value of n would have to match the number of rows if wanted to do for actual patients.

#plt.xkcd()

d_nom = 2

cal_point1 = 54 # fraction 27 = approx 54Gy
cal_point2 = 58 # fraction 31 = approx 58Gy

meas_d_list = [d_nom]*37 # start with all nominal doses
missed_fracs = [30,31] # state which fractions are missed
hypo_fracs = [32,33,34,35,36,37] # state which fractions are hypo

## repalce missed fractions with zero dose
for i in missed_fracs:
    meas_d_list[i-1] = 0

for i in hypo_fracs:
    meas_d_list[i-1] = 2.5 

#meas_d_list1 = [2]*27 # standard fractions
#meas_d_list2 = [0]*2 # missed fractions
#meas_d_list3 = [2.5]*10 # hypofracitonation (dose value could be calcualted from BED?)
#meas_d_list = meas_d_list1 + meas_d_list2 + meas_d_list3
#print(meas_d_list)

d_list_type = meas_d_list
#d_list_type = None

d_int = 74

d_use = [None,d_list_type] # for plotting standard and list of doses on same plot

for j in d_use:

    TCP_results1 = TCP.completeTCPcalc(n=1000,
                                  alphabeta_use=3,
                                  alphabeta_sd_use=0.5,
                                  d=d_nom,
                                  d_shift=0, # no shift as want standard only
                                  d_sd=0.5,
                                  d_trend=0,
                                  max_d=100,
                                  dose_of_interest=d_int,
                                  TCP_input = 70.0,
                                  d_list = j,
                                  n0 = 170)
    

    #print(TCP_results1[12])
    ## only plot the results in which dose is delivered
    if j is not None:
        x_filt = TCP_results1[13][TCP_results1[13]<=d_int]
        y_filt = TCP_results1[12][TCP_results1[13]<=d_int]
        plt.plot(x_filt,y_filt, marker='o', color='green')
    else:
        plt.plot(TCP_results1[13],TCP_results1[12], color='blue')

    ## plot some marker lines to indicate key points
    plt.plot([74,74],[0.0,1.0],ls='--', color='black')
    
    ## indicate missed fractions
    for i in missed_fracs:
        plt.plot([d_nom*(i),d_nom*(i)],[0.0,1.0],ls='--',color='red')
    #plt.plot([cal_point1,cal_point1],[0.0,1.0],ls='--')
    #plt.plot([cal_point2,cal_point2],[0.0,1.0],ls='--')
    plt.title('Demo showing missed fractions and hyperfractionation')
    plt.xlabel('Nominal Dose')
    plt.ylabel('TCP')

## save plots in multiple formats

#for ext in ['eps','png','pdf']:
#    plt.savefig(r'C:\Users\mb22\OneDrive\PhD\Quasar Shared\missed_frac+hypo.' + ext)

## save doses
#np.savetxt(r'C:\Users\mb22\OneDrive\PhD\Quasar Shared\Modelling\IPython\OPs\varied_dose_tcps_std_doses.csv', TCP_results1[13])
## TCPs
#np.savetxt(r'C:\Users\mb22\OneDrive\PhD\Quasar Shared\Modelling\IPython\OPs\varied_dose_tcps_std_TCPs.csv', TCP_results1[12])
#%%

## perform the analysis with multiple parameter variations and save as CSV file.

print("Started....")


#CHHIP: node negative T1b-T3a localised PCa
# with risk of seminal vesical involvement ≤30%

all_test = TCP.TCP_full(k=2,
                    TCP_input=88.3,
                    repeats=5,
                    n=500,
                    n0 = 150,
                    alphabeta_use=3,
                    alphabeta_sd_use=0.5,
                    d=2,
                    d_shift=0,
                    d_sd=0,
                    d_trend=0,
                    max_d=100,
                    dose_of_interest=74,
                    save_name="Results16July16-CHHIP_74-Trend=0-ab_sdvar+d_sd0123")

print("Completed....")

#%%
## load CSV file into pandas for analysis
          
TCP_data = pd.read_csv(os.getcwd()+"\\"+all_test[0]) # read in file saved after TCP simulation.

print(all_test[0])
TCP_data.describe()

#%%
