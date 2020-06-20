import math as m
import random as rd
import matplotlib.pyplot as plt
import sys
import pandas as pd
import copy
df=pd.read_csv("dataset1.csv")
def diff_length_location(a,b):
    return m.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
def generation_number(k_number):
    k=[]
    i=0
    while i <k_number:
        ltemporary=[rd.uniform(-7.5,10),rd.uniform(-7.5,10)]
        k.append(ltemporary)
        i +=1
        for mlv in range(i-1):
            if ltemporary==k[mlv]:
                i -=1
                k.pop()
                print ("it works")
                break
    return k
class clusters_users:
    def __init__(self,x):
        self.point=copy.deepcopy(x)
        self.head=0
    def re_arrange(self,hds):
        min=diff_length_location(self.point,hds[0])
        self.head=copy.deepcopy(hds[0])
        for i in hds:
            temporary=diff_length_location(self.point,i)
            if min>temporary:
                min=temporary
                self.head=copy.deepcopy(i)
class k_means():
    def __init__(self,df):
        it_array=[]
        cost_array=[]
        for i in range(1,11):
            cheads=generation_number(i)
            ordinates=df.values
            allordinates=[]
            for i in ordinates:
                allordinates.append(clusters_users(i))
            for i in allordinates:
                i.re_arrange(cheads)
            old_c=0
            for i in cheads:
                for j in allordinates:
                    if j.head==i:
                        old_c +=diff_length_location(i,j.point)
            old_heads=[]
            old_heads=copy.deepcopy(cheads)
            for i in range(len(cheads)):
                count=0
                mean=[0,0]
                for j in allordinates:
                    if j.head==cheads[i]:
                        mean[0]+=j.point[0]
                        mean[1]+=j.point[1]
                        count +=1
                try:
                    cheads[i][0]=mean[0]/count
                    cheads[i][1]=mean[1]/count
                except:
                    k_means(df)
                    print ("Bad Cluster Head Initialization")
                    sys.exit(1)
            new_c=0
            for i in allordinates:
                    i.re_arrange(cheads)
            new_c=0
            for i in cheads:
                for j in allordinates:
                    if j.head==i:
                        new_c +=diff_length_location(i,j.point)
            mean=[0,0]
            for i in range(len(cheads)):
                count=0
                mean=[0,0]
                for j in allordinates:
                    if j.head==cheads[i]:
                        mean[0]+=j.point[0]
                        mean[1]+=j.point[1]
                        count +=1
                try:
                    cheads[i][0]=mean[0]/count
                    cheads[i][1]=mean[1]/count
                except:
                    k_means(df)
                    print ("Please ignore this exception message caued due to Bad Cluster Head Initialization")
                    sys.exit(1)
            iterations=2
            while abs(old_c-new_c)>0.01:
                old_c=new_c
                for i in allordinates:
                    i.re_arrange(cheads)
                new_c=0
                for i in cheads:
                    for j in allordinates:
                        if j.head==i:
                            new_c +=diff_length_location(i,j.point)
                mean=[0,0]
                count=0
                for i in range(len(cheads)):
                    count=0
                    mean=[0,0]
                    for j in allordinates:
                        if j.head==cheads[i]:
                            mean[0]+=j.point[0]
                            mean[1]+=j.point[1]
                            count +=1
                    try:
                        cheads[i][0]=mean[0]/count
                        cheads[i][1]=mean[1]/count
                    except:
                        k_means(df)
                        print ("Bad Cluster Head Initialization")
                        sys.exit(1)
                iterations+=1
            it_array.append(iterations)
            cost_array.append(new_c)
        clusters = [i+1 for i in range(10)]
        fig, ax1 = plt.subplots()
        ax1.plot(clusters, it_array, color='red', label = "Iterations")
        ax1.set_xlabel("Number of Cluster(k)")
        ax1.set_ylabel("Number of Iterations")
        ax1.tick_params(axis='y', labelcolor='red')
        ax2 = ax1.twinx()
        ax2.set_ylabel("Cost Function")
        ax2.plot(clusters, cost_array, color='green', label = "Cost")
        ax2.tick_params(axis='y', labelcolor='green')
        fig.legeneration_numberd()
        fig.tight_layout()
        ratios=[]
        for lit in range(2,9):
            r=abs((cost_array[lit]-cost_array[lit+1])/(cost_array[lit-1]-cost_array[lit]))
            ratios.append(r)
        mlii=ratios.index(min(ratios))
        print ("")
        print ("The minimum cost occur at ",mlii+2," no of Clusters")
k_means(df)
