'''
Created on Sep 30, 2015

@author: arya
'''
import pandas as pd
import numpy as np
import sys,pickle,os
from statsmodels.regression.tests.test_quantile_regression import idx
path='/home/arya/PubMed/GEO/Datasets/'
outpath=path+'prefOut/'
if not os.path.exists(outpath):            os.makedirs(outpath)
from scikits.crab import datasets
from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import pearson_correlation, cosine_distances
from scikits.crab.similarities import UserSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender
from ranking.Measure import AP,MRR
from multiprocessing import  Pool

numFeedbacks=5
def createUserDataMatrix():
    p =pd.read_pickle(path+'PA.df')
    dp =pd.read_pickle(path+'DPP.df')
    dp=dp[['accession','cites_pmid']]
    p['author']=p[['name','family']].dropna().apply( ' '.join, axis=1)
    p=p[['pmid','author']]

    da=pd.merge(p,dp,left_on='pmid',right_on='cites_pmid')[['accession','author']]
    

    da=pd.DataFrame(da.values.astype('unicode'),columns=['accession','author'])
    
    da['da']=da.apply( ' '.join, axis=1)
    da
    rating = da.groupby(['da']).da.agg('count')
    
    da.index=da.da
    da.ix[rating.index,'rating']=rating
    

    
    
    da.drop_duplicates(cols='da', inplace=True)
    da.index=range(da.shape[0])
    da.drop('da',axis=1,inplace=True)
    da
    idx=da.author.value_counts()>10
    da=pd.merge(da,pd.DataFrame(idx[idx].index,columns=['author']),on='author')
    da.to_pickle(path+'DA_RatingRelation.df')
    da=pd.read_pickle(path+'DA_RatingRelation.df')
    
    idx=da.author.value_counts()>50
    da=pd.merge(da,pd.DataFrame(idx[idx].index,columns=['author']),on='author')

    sample=np.sort(np.random.choice(da.author.unique().shape[0],200,False))
    sample=da.author.unique()[sample]
    da =pd.merge(da,pd.DataFrame(sample,columns=['author']),on='author')
    
    M=pd.DataFrame(0.0,columns=da.author.unique(),index=da.accession.unique())
    print M.shape
    for _,row in da.iterrows():
        M.ix[row.accession,row.author]=row.rating
    sample=np.sort(np.random.choice(M.shape[0],1000,False))
    M=M.iloc[sample]
    M.to_pickle(path+'DA_Rating.df')
    

def getRecommenderData(df):
    data=df.to_dict()
    for user,prefs in data.items():
        for k,v in prefs.items():
            if not v:
                del data[user][k]
    return data

def recom(i):
    try:
        M=pd.read_pickle(path+'DA_Rating.df')
        user=M.ix[:,i]
        user.name
        usernnz=user>0
        usernnzIDX=np.where(usernnz)
        targets=user[usernnz].index.values
        N=M.copy()
        N.ix[:,i]=0
        idx=np.random.random_integers(0,len(usernnzIDX[0]),min(len(usernnzIDX[0])-3,numFeedbacks))
        N.ix[idx,i]=user.iloc[idx]
        model = MatrixPreferenceDataModel(getRecommenderData(N))
        similarity = UserSimilarity(model,  cosine_distances, 3)
        recommender = UserBasedRecommender(model, similarity, with_preference=True)
        rec=recommender.recommend( user.name, how_many=100)
        ranking=map(lambda x: x[0],rec)
        ap,mrr=AP(ranking,targets) , MRR(ranking,targets)
        pd.to_pickle((ap,mrr), outpath+'numFB{}i{}.pkl'.format(numFeedbacks,i))
    except:
        pass

def merge():
    APs,MRRs=[],[]
    for i in range(200):
        try:
            res=pd.read_pickle(outpath+'numFB{}i{}.pkl'.format(numFeedbacks,i))
            if res[0]:
                APs.append(res[0])
                MRRs.append(res[1])
        except:
            pass
    pd.to_pickle( {'AP':{'mean':np.mean(APs),'std':np.std(APs)}, 'MRR':{'mean':np.mean(MRRs),'std':np.std(MRRs)}},'/home/arya/PubMed/prefFB{}.pkl'.format(numFeedbacks))

    
if __name__ == '__main__':
    #Pool(15).map(recom,range(200))
    print 
    from scikits.crab import datasets
    movies = datasets.load_sample_movies()
    from scikits.crab.models import MatrixPreferenceDataModel
    model = MatrixPreferenceDataModel(movies.data)
    from scikits.crab.metrics import pearson_correlation
    from scikits.crab.similarities import UserSimilarity
    similarity = UserSimilarity(model, pearson_correlation)
    
    from scikits.crab.recommenders.knn import UserBasedRecommender
    recommender = UserBasedRecommender(model, similarity, with_preference=True)
    recommender.recommend(5)