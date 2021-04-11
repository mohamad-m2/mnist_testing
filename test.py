import csv 
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import math
import functools as f
import scipy.linalg as sc 

def show_pca_rank(n,dev,z1):
    k=np.zeros((50));
    
    for i in dev:
        for j in dev[i]:
            k=k+abs(j.T);
    k=(k*100)/k.sum()
    print(k.shape)
    m=np.array([i.reshape((28,28)) for i in n.T])
    figure, axes = plt.subplots(nrows=5, ncols=10,sharex=True, sharey=True)
    j=0
    for i in m:
        axes[j//10,j%10].imshow(i,cmap='gray')
        axes[j//10,j%10].set_title(str(round(k[0,j],1))+'%')
        j=j+1
    figure.tight_layout(pad=z1)
        
def show_pca(n):
    m=np.array([i.reshape((28,28)) for i in n.T])
    figure, axes = plt.subplots(nrows=5, ncols=10)
    j=0
    for i in m:
        axes[j//10,j%10].imshow(i,cmap='gray')
       
        j=j+1
 
def show_lda(u,n):
    x=[]
    for i in u.T:
        x.append(np.dot(i,n.T).reshape((28,28)))
    
    m=np.array(x)
    figure, axes = plt.subplots(nrows=5, ncols=2)
    j=0
    for i in m:
        axes[j%5,j//5].imshow(i,cmap='gray')
       
        j=j+1  
 
#trans emlement or dictionary       
def trans_dic(dic,n):
    dv={i:[np.dot(n.T,k.reshape((784,1))) for k in dic[i]] for i in dic}
    return dv

def trans_dic_lda(dic,u):
    dv={i:[np.dot(u.T,k.reshape((50,1))) for k in dic[i]] for i in dic}
    return dv
    

def trans(n1,n2):
    figure, axes = plt.subplots(nrows=1, ncols=2)
    
    
    axes[0].imshow(n1,cmap='gray')
    axes[1].imshow(n2,cmap='gray')

def trans_pca(n,x):
    k=np.dot(n.T,x.reshape((784,1)))
    d=np.dot(n,k)
    d=d.reshape((28,28))  
    return d

def trans_lda(u,n,x):
    x=np.dot(u,x)
    x=np.dot(n,x)    
    d=x.reshape((28,28))  
    return d

###################################
    
 # extract x dim from cov matrix 
def highst_m(co,x):
        m,n=np.linalg.eigh(co)

        return (n.T[-1:-(x+1):-1]).T
             

#######################   
 
# scatter cov matrix
    
def extract(co):
    meanc=sum([sum([abs(k) for k in f]) for f in co])/co.size
    x=[]
    y=[]
    val=[]
    for idx,i in enumerate(co):
        for idy,j in enumerate(i):
            if(abs(j)>10*meanc):
                x.append(idx)
                y.append(idy)
                val.append(math.log(abs(j)))
    plt.figure()
    plt.scatter(x,y)
    
#################
    
def calc_between(dic):
    mean_class=[]
    count=[]
    for i in dic.keys():
        count.append(np.array(dic[i]).shape[0])
        mean_class.append(np.array(dic[i]).mean(axis=0))
        
    mean_class=np.array(mean_class)
    mean_tot=mean_class.mean(axis=0)
    
    result=0
    for idx,i in enumerate(mean_class):

        x=i.reshape((i.size,1))-mean_tot.reshape((mean_tot.size,1))
        result+=count[idx]*np.dot(x,x.T)
    
    return  result/sum(count)

def calc_within(dic):
    mean_class=[]
    count=0
    for i in dic.keys():
        count+=np.array(dic[i]).shape[0]
        mean_class.append(np.array(dic[i]).mean(axis=0))
        
    mean_class=np.array(mean_class)
    
    result=0
    for idx,i in enumerate(dic.keys()):
        for j in dic[i]:
           
            x= j.reshape((j.size,1))-mean_class[idx].reshape((mean_class[idx].size,1))
            result+=np.dot(x,x.T)
    
    return  result/count


def compute_lda(x,y,m):
    
    s,u=sc.eigh(x,y)    
    return u[:,-1:-(m+1):-1]

def div(x,nb):
    z={i:x[i][0:-nb] for i in x.keys()}
    f={i:x[i][-nb:] for i in x.keys()}
    return z,f

def model(x):
    m= [np.array(x[i]).mean(axis=0) for i in x.keys()]
    var=[]
    for idx,i in enumerate(x.keys()):
        var.append(0)
        for j in  x[i]:
            var[idx]+=np.dot((j-m[idx]),(j-m[idx]).T)
        var[idx]=var[idx]/len(x[i])
    param={i:j for i,j in enumerate(zip(m,var))}
    return param

def predict_label(x,param,prior):
    
    score={}
    for i in param.keys():
        m=param[i][0]
        v=param[i][1]
        x1=x-m
        x2=-0.5*np.dot(np.dot(x1.T,np.linalg.inv(v)),x1)
        x2=np.exp(x2)
        x2=x2/(2*np.pi)**(x.size/2)
        x2=x2/(np.linalg.det(v))**0.5
        score[i]=x2*prior
    inverse = [(value, key) for key, value in score.items()]
    return max(inverse)[1]


a= csv.reader(open('mnist.csv','r'),delimiter=',')
next(a)

dic={}
for b in a:
    
    c=np.array([float(x) for x in b[:-1]]).reshape((28,28))
    if(dic.get(float(b[-1]),0)==0):
        dic[float(b[-1])]=[]
    else:
        dic[float(b[-1])].append(c)
   

#plt.imshow(dic[2][0],cmap='gray')


mean=f.reduce(lambda x,y: x+y,f.reduce(lambda x,y:x+y,dic.values())) 
mean=mean/sum([len(i) for i in dic.values()])

# centeralize data
dic_center={i:[k-mean for k in dic[i]] for i in dic}
#end

#calc cov

temp=f.reduce(lambda x,y:x+y,dic_center.values())
cov=0
for i in temp:
    cov+=np.dot(i.reshape((784,1)),i.reshape((1,784)))
    
cov=cov/(sum([len(dic_center[i]) for i in dic_center]))

n=highst_m(cov,50)
pca_dic=trans_dic(dic,n)
sw=calc_within(pca_dic)
sb=calc_between(pca_dic)
u=compute_lda(sb,sw,10)
UW, _, _ = np.linalg.svd(u)
U = UW[:, 0:10]

lda_dic=trans_dic_lda(pca_dic,U)


train,test=div(lda_dic,50)
par=model(train)




acc=0
count=0
acc2=[]
c=0
for idx,i in enumerate(test.keys()):
    count+=len(test[i])
    c=len(test[i])
    acc2.append(0)
    for j in test[i]:
       if( predict_label(j,par,0.1)==i):
           acc+=1
           acc2[idx]+=1
    acc2[idx]/=c
           
acc=acc/count

#end

for i in range(4):
    c=random.randrange(400)
    z1=dic[6][c]
    z2= trans_lda(U,n ,lda_dic[6][c])
    trans(z1,z2)


 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             