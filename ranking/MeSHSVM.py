'''
Created on Jun 26, 2015

@author: arya
'''
from sklearn.externals import joblib
import os ,sys
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import  LinearSVC
from sklearn.datasets import load_svmlight_file
import numpy as np
from time import time
import pandas as pd

from sklearn.preprocessing import  MultiLabelBinarizer 

def correct_dataset(path):
    lines=open(path).readlines()
    with open(path,'w') as f:
        for line in lines:
            print >> f,line.replace(', ', ',').strip()
def correct_all():            
    path='/home/arya/PubMed/GEO/Datasets/'
    multilabel=True
    for fold in range(5):
        dspath='{}libsvm/train.{}.{}.libsvm'.format(path,fold, ('multiclass','multilabel')[multilabel])
        correct_dataset(dspath)
        correct_dataset(dspath.replace('train', 'test'))
        
def remove_unknown_classes(y, labels):        
    len(y)
    labels.shape
    new_y=[]
    for i in range(len( y)):
        sample_y=[]
        for l in y[i]:
            if l in labels:
                sample_y.append(l)
        new_y.append(sample_y)
    return new_y    
        
    
def compute_ranking(learnFullModel=False):
    path='/home/arya/PubMed/GEO/Datasets/'
    modelpath=path+'libsvm/model/'
    if not os.path.exists(modelpath):            os.makedirs(modelpath)
    outpath='{}libsvm/out/'.format(path)
    sys.stdout=open('{}SVM.log'.format('/home/arya/PubMed/GEO/Log/'),'w')
    sys.stderr=open('{}SVM.err'.format('/home/arya/PubMed/GEO/Log/'),'w')
    if not os.path.exists(outpath):            os.makedirs(outpath)
    X, Y = load_svmlight_file(path+'Corpus.libsvm',multilabel=True)
    Y=np.array(Y)
    if learnFullModel:
        model=OneVsRestClassifier(LinearSVC(random_state=0)).fit(X, Y)
        joblib.dump(model, modelpath+'Model.libsvm')
        print 'The Full Model is Saved!'
    Folds=pd.read_pickle(path+'Folds.df')
    for fold in range(Folds.shape[1]):
        start=time()
        Xtr,Ytr=X[Folds[fold].values,:],Y[Folds[fold].values]
        print 'learning on fold...',Xtr.shape,fold, sys.stdout.flush()
        model=OneVsRestClassifier(LinearSVC(random_state=0)).fit(Xtr, Ytr)
        Xte=X[~Folds[fold].values,:]
        labels=model.classes_
#         Yte=remove_unknown_classes(Yte, labels)
#         idx=np.array(map(lambda x: len(x)>0,Yte))
#         Yte=np.array(Yte)[idx]
#         Xte=Xte[idx]
        print 'predicting...',Xte.shape, sys.stdout.flush()
        pd.DataFrame(columns=labels,data=model.decision_function(Xte)).to_pickle('{}deci.{}.df'.format(outpath,fold))
#         (pd.DataFrame(columns=labels,data=MultiLabelBinarizer().fit_transform(list(Yte)+[labels]))).iloc[:-1].to_pickle('{}labels.{}.df'.format(outpath,fold))
#         ranking.to_pickle('{}ranking.{}.df'.format(outpath,fold))
        print 'Done in {:.0f} minutes'.format((time()-start)/60.0)



if __name__ == '__main__':
    compute_ranking()
    print 'Done'
