#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import random
import math
import csv
import itertools
import copy
import os
import glob

 
def findsubsets(s, n):
    return list(itertools.combinations(s, n))

def simulate_ER(n,prob, opq_prob, opq_Set,S, iteration):
    R_list = []
    num_choice = n + len(opq_Set)
    population = list(range(num_choice))
    weight = prob+opq_prob
    for t in range(iteration):
        inv = [S for i in range(n)]
        flag = 1
        while flag ==1:
            choice =  random.choices(population, weights=weight, k=1)[0]
            if choice<n:
                inv[choice] = inv[choice]-1
            else:
                choice = opq_Set[choice-n]
                index_max = np.argmax([inv[index] for index in choice])
                inv[choice[index_max]] = inv[choice[index_max]] -1
            if min(inv)==0:
                R_list.append(n*S-sum(inv))
                flag = 0   
    return(np.average(R_list), np.average([i**2 for i in R_list]))


def cost(n,h,K,lamb, S, ER,ER2):
    holding = (2*n*S+1)*ER-ER2
    holding = float(h*holding)/(2*lamb*ER)
    ordering = float(K)/ER
    return(holding+ordering, holding, ordering)

## simulation set up
n=7
K=1000
h=1
lamb=1
S = 100 
iteration = 10000
qlist = [0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

#categorical overlap less
scenario1 = []
opq_Set = [[0,1,2,3],[3,4,5,6]]
for q in qlist:
    prob = [float(1-q)/n for i in range(n)]
    opq_prob = [q/2, q/2]
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario1.append(cost(n,h,K,lamb, S, ER,ER2)[0])
print(scenario1)

#categorical overlap more
scenario2 = []
opq_Set = [[0,1,2,3,4],[2,3,4,5,6]]
for q in qlist:
    prob = [float(1-q)/n for i in range(n)]
    opq_prob = [q/2, q/2]
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario2.append(cost(n,h,K,lamb, S, ER,ER2)[0])
print(scenario2)

    
#n-opq
scenario3 = []
opq_Set = [[0,1,2,3,4,5,6]]
for q in qlist:
    prob = [float(1-q)/n for i in range(n)]
    opq_prob = [q]
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario3.append(cost(n,h,K,lamb, S, ER,ER2)[0])
print(scenario3)
    
#circle model
scenario4 = []
opq_Set = [[i,i+1] for i in range(n-1)]
opq_Set.append([0,6])
for q in qlist:
    prob = [float(1-q)/n for i in range(n)]
    opq_prob = [q/n for i in range(n)]
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario4.append(cost(n,h,K,lamb, S, ER,ER2)[0])
print(scenario4)

################################################################
# plot Figure 4a in paper
benchmark = scenario4[0]
d1 = [100*(1-i/benchmark) for i in scenario3]
d2 = [100*(1-i/benchmark) for i in scenario2]
d3 = [100*(1-i/benchmark) for i in scenario1]
d4 = [100*(1-i/benchmark) for i in scenario4]
t = qlist

fig = plt.figure(figsize=(6, 5))
ax = plt.subplot(1, 1, 1)
y=plt.plot(t,d1, 'or-',t,d2,'sb-',t,d3, '^g-', t, d4, '*c-')
plt.ylabel('Relative Cost Savings (%)', fontsize = 14)
plt.xlabel('$q$', fontsize = 14)
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.axhline(y=d1[-1],color='k', linestyle='--')
plt.ylim(0,11)
plt.xlim(0,1.01)
plt.legend(y,['n-opq','categorical $w=3/7$','categorical $w=1/7$', 'circle'],loc='best', fontsize=14,shadow=True, fancybox=True)
plt.show()
fig.savefig('fig4a.pdf',bbox_inches='tight') 

################################################################
# plotting Figure 4b in paper
benchmark = scenario4[0]
d1 = [0]+ [100*(1-i/benchmark) for i in qresult[1]]+[100*(1-scenario3[1]/benchmark)]
d2 = [0]+ [100*(1-i/benchmark) for i in qresult[2]]+[100*(1-scenario3[2]/benchmark)]
d3 = [0]+ [100*(1-i/benchmark) for i in qresult[5]]+[100*(1-scenario3[5]/benchmark)]
d4 = [0]+ [100*(1-i/benchmark) for i in qresult[10]]+[100*(1-scenario3[10]/benchmark)]
t = [1,2,3,4,5,6,7]
fig = plt.figure(figsize=(6, 5))
ax = plt.subplot(1, 1, 1)
y=plt.plot(t,d1, 'oc-',t,d2,'sb-',t,d3, '^g-', t, d4, '*r-')
plt.ylabel('Relative Cost Savings (%)', fontsize = 14)
plt.xlabel('$k$', fontsize = 14)
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylim(0,11)
plt.xlim(1,7.1)
plt.legend(y,['$q=0.1$','$q=0.2$','$q=0.5$', '$q=1.0$'],loc='best', fontsize=14,shadow=True, fancybox=True)
plt.show()
fig.savefig('fig4b.pdf',bbox_inches='tight') 


