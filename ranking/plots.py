'''
Created on Jul 9, 2015

@author: arya
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pickle as pk
import pandas as pd
path='/home/arya/PubMed/'
def plot(y,MAP=True,fontsize=30,figsize=(18, 10), dpi=80):
    plt.figure(figsize=figsize, dpi=dpi)
    mpl.rc('font', **{'family': 'serif', 'serif': ['Times'], 'size':fontsize})
    
    m =y.mean( axis=1)
    print m
    title=["MRR","MAP"][MAP]
    labels = ['GEO', 'Jaccard', 'R', 'RI', 'Pref1','Pref5','RIP1' ,'RIP5' ]
    x = range(len(labels))
    error=y.std(axis=1)/2
    pref=[pd.read_pickle(path+'prefFB{}.pkl'.format(i)) for i in [1,5]]
    print pref
    prefm=map(lambda x: x[('AP','MRR')[not MAP]]['mean'] , pref)
    prefs=map(lambda x: x[('AP','MRR')[not MAP]]['std'] /2, pref)
    print prefm
    m=np.append(m,prefm)
    error=np.append(error,prefs)
    
    rip=[pd.read_pickle(path+'RIP{}.pkl'.format(i)) for i in [1,5]]
    prefm=map(lambda x: x[('AP','MRR')[not MAP]]['mean'] , rip)
    prefs=map(lambda x: x[('AP','MRR')[not MAP]]['std'] /2, rip)
    m=np.append(m,prefm)
    error=np.append(error,prefs)
    
    plt.errorbar(x,m, yerr=error, fmt='ok',linewidth=2, markersize=15)
    plt.xlim([-1,len(x)])
    plt.ylim([-0.01,max(m)+max(error)+0.05])
    plt.grid()
    plt.xticks(x, labels)
    plt.title(title)
    plt.savefig(path+title+'.png')
    plt.show()
    

if __name__ == '__main__':
    y=pk.load(open(path+'MRR.pkl'))
    plot(y,MAP=False)
    y=pk.load(open(path+'MAP.pkl'))
    plot(y,MAP=True)
    