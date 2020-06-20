import random as rd
import matplotlib.pyplot as plt
import copy
import sys
import pandas as pd
import math as m
class existing_users:
    def __init__(self,x):
        self.point=copy.deepcopy(x)
        self.head=0

    def re_arrange(self,hds):
        least=lengthtoit(self.point,hds[0])
        self.head=copy.deepcopy(hds[0])
        for i in hds:
            temp=lengthtoit(self.point,i)
            if least>temp:
                least=temp
                self.head=copy.deepcopy(i)

item_set=pd.read_csv("dataset1.csv")
def lengthtoit(a,b):
    return m.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
def gen(k_number):
    k=[]
    i=0
    while i <k_number:
        ltemp=[rd.uniform(-7.5,10),rd.uniform(-7.5,10)]
        k.append(ltemp)
        i +=1
        for mlv in range(i-1):
            if ltemp==k[mlv]:
                i -=1
                k.pop()
                print ("it works")
                break
    return k

class kinitial_avgs():
    def __init__(self,item_set):
        it_array=[]
        cost_array=[]
        for i in range(1,11):
            consumer_heads=gen(i)
            ordinates=item_set.values
            hj_dist_manip=[]
            for i in ordinates:
                hj_dist_manip.append(existing_users(i))
            for i in hj_dist_manip:
                i.re_arrange(consumer_heads)
            old_c=0
            for i in consumer_heads:
                for j in hj_dist_manip:
                    if j.head==i:
                        old_c +=lengthtoit(i,j.point)
            old_heads=[]
            old_heads=copy.deepcopy(consumer_heads)
            for i in range(len(consumer_heads)):
                count=0
                initial_avg=[0,0]
                for j in hj_dist_manip:
                    if j.head==consumer_heads[i]:
                        initial_avg[0]+=j.point[0]
                        initial_avg[1]+=j.point[1]
                        count +=1
                try:
                    consumer_heads[i][0]=initial_avg[0]/count
                    consumer_heads[i][1]=initial_avg[1]/count
                except:
                    kinitial_avgs(item_set)
                    print ("Please ignore this exception message caued due to Bad Cluster Head Initialization")
                    sys.exit(1)
            new_c=0
            for i in hj_dist_manip:
                    i.re_arrange(consumer_heads)
            new_c=0
            for i in consumer_heads:
                for j in hj_dist_manip:
                    if j.head==i:
                        new_c +=lengthtoit(i,j.point)
            initial_avg=[0,0]
            for i in range(len(consumer_heads)):
                count=0
                initial_avg=[0,0]
                for j in hj_dist_manip:
                    if j.head==consumer_heads[i]:
                        initial_avg[0]+=j.point[0]
                        initial_avg[1]+=j.point[1]
                        count +=1
                try:
                    consumer_heads[i][0]=initial_avg[0]/count
                    consumer_heads[i][1]=initial_avg[1]/count
                except:
                    kinitial_avgs(item_set)
                    print ("Bad Cluster Head Initialization")
                    sys.exit(1)
            itr=2
            while abs(old_c-new_c)>0.01:
                old_c=new_c
                for i in hj_dist_manip:
                    i.re_arrange(consumer_heads)
                new_c=0
                for i in consumer_heads:
                    for j in hj_dist_manip:
                        if j.head==i:
                            new_c +=lengthtoit(i,j.point)
                initial_avg=[0,0]
                count=0
                for i in range(len(consumer_heads)):
                    count=0
                    initial_avg=[0,0]
                    for j in hj_dist_manip:
                        if j.head==consumer_heads[i]:
                            initial_avg[0]+=j.point[0]
                            initial_avg[1]+=j.point[1]
                            count +=1
                    try:
                        consumer_heads[i][0]=initial_avg[0]/count
                        consumer_heads[i][1]=initial_avg[1]/count
                    except:
                        kinitial_avgs(item_set)
                        print ("Bad Cluster Head Initialization")
                        sys.exit(1)
                itr+=1
            it_array.append(itr)
            cost_array.append(new_c)
        clst = [i+1 for i in range(10)]
        fig, axis_one_to1 = plt.subplots()
        axis_one_to1.plot(clst, it_array, color='red', label = "itr")
        axis_one_to1.set_xlabel("Cluster(k)")
        axis_one_to1.set_ylabel("itr")
        axis_one_to1.tick_params(axis='y', labelcolor='red')
        axis_one_to2 = axis_one_to1.twinx()
        axis_one_to2.set_ylabel("CF")
        axis_one_to2.plot(clst, cost_array, color='green', label = "Cost")
        axis_one_to2.tick_params(axis='y', labelcolor='green')
        fig.legend()
        fig.tight_layout()
        ratios=[]
        for lit in range(2,9):
            r=abs((cost_array[lit]-cost_array[lit+1])/(cost_array[lit-1]-cost_array[lit]))
            ratios.append(r)
        mlii=ratios.index(min(ratios))
        print ("Minimum cost at ",mlii+2," no of clst")
kinitial_avgs(item_set)
