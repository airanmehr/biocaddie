'''
Created on Jun 29, 2015

@author: arya
'''
from Bio import Entrez
import numpy as np
Entrez.email="a@a.com"
a=['GSE63882', 'GSE69636', 'GSE69633', 'GSE66492', 'GSE62399', 'GSE50011', 'GSE67472', 'GSE52319', 'GSE45329', 'GSE55762', 'GSE65124', 'GSE44134', 'GSE44133', 'GSE42172', 'GSE42334', 'GSE42333', 'GSE52509', 'GSE62182', 'GSE56099', 'GSE51601', 'GSE55962', 'GSE56782', 'GSE50254', 'GSE55127', 'GSE55454', 'GSE44603', 'GSE49107', 'GSE35222', 'GSE50836', 'GSE51530', 'GSE28368', 'GSE43411', 'GSE49450', 'GSE42623', 'GSE42668', 'GSE42667', 'GSE45330', 'GSE47022', 'GSE45847', 'GSE43688', 'GSE42962', 'GSE42889', 'GSE40407', 'GSE41421', 'GSE34517', 'GSE37058', 'GSE38093', 'GSE18033', 'GSE39455', 'GSE33512', 'GSE37768', 'GSE38409', 'GSE34642', 'GSE30079', 'GSE36568', 'GSE36810', 'GSE26887', 'GSE27681', 'GSE36174', 'GSE28804', 'GSE33561', 'GSE34635', 'GSE28906', 'GSE30272', 'GSE13931', 'GSE31548', 'GSE31547', 'GSE31908', 'GSE30660', 'GSE30906', 'GSE30032', 'GSE20257', 'GSE19407', 'GSE27272', 'GSE27973', 'GSE24414', 'GSE27002', 'GSE19667', 'GSE23611', 'GSE21066', 'GSE21532', 'GSE20143', 'GSE20520', 'GSE17913', 'GSE18344', 'GSE19510', 'GSE19540', 'GSE18235', 'GSE18044', 'GSE12930', 'GSE12587', 'GSE12586', 'GSE12585', 'GSE17484', 'GSE13896', 'GSE14461', 'GSE14383', 'GSE14385', 'GSE11952', 'GSE15563', 'GSE13260', 'GSE13309', 'GSE8790', 'GSE14634', 'GSE10135', 'GSE7832', 'GSE12428', 'GSE10063', 'GSE12036', 'GSE8987', 'GSE11798', 'GSE10896', 'GSE10718', 'GSE10700', 'GSE7310', 'GSE7079', 'GSE7895', 'GSE7434', 'GSE6854', 'GSE4806', 'GSE4234', 'GSE4516', 'GSE4644', 'GSE3212', 'GSE2302', 'GSE2090', 'GSE1276', 'GSE994']
t=a[7:100:5]
def query_geo(query):
    query =r"gse " +query
    handle = Entrez.esearch(db='gds',term=query,retmax=1000)
    records = Entrez.read(handle)
    handle.close()
    records = records['IdList']
    handle = Entrez.efetch(db='gds',id=records, retmode="xml")
    return [i.split()[2] for i in handle if i[:6]=='Series']

def AP(ranking, targets, k=20):
    """average precision"""
    ranking=np.array(ranking[:k])
    results=np.array([])
    for tt in targets:
        results =np.append(results, np.where(ranking==tt)[0])
    results +=1
    print '{} hits in top {}'.format(len(results),k)
    return  len(results)/float(k)
        

def MRR(ranking, targets, k=20):
    """mean reciprocal rank"""
    """average precision"""
    ranking=np.array(ranking[:k])
    results=np.array([k])
    for tt in targets:
        results =np.append(results, np.where(ranking==tt)[0])
    results +=1
    print '{} is 1st hit in top {}'.format(min(results),k)
    return  1.0/min(results)
        
if __name__ == '__main__':
    print AP(a,t)
    print MRR(a,t)
    print 'Done'
