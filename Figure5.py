#!/usr/bin/env python
# coding: utf-8

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
n=7
K=1000
h=1
lamb=1
# S = 100 
iteration = 10000
q = 0.2
Slist = [50,100, 150, 200, 250 , 300]

#categorical overlap less
scenario1 = []
opq_Set = [[0,1,2,3],[3,4,5,6]]
prob = [float(1-q)/n for i in range(n)]
opq_prob = [q/2, q/2]
for S in Slist:
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario1.append(cost(n,h,K,lamb, S, ER,ER2))

#categorical overlap more
scenario2 = []
opq_Set = [[0,1,2,3,4],[2,3,4,5,6]]
prob = [float(1-q)/n for i in range(n)]
opq_prob = [q/2, q/2]
for S in Slist:
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario2.append(cost(n,h,K,lamb, S, ER,ER2))
    
# n opq
scenario3 = []
opq_Set = [[0,1,2,3,4,5,6]]
prob = [float(1-q)/n for i in range(n)]
opq_prob = [q]

for S in Slist:
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario3.append(cost(n,h,K,lamb, S, ER,ER2))
    
#chain
scenario4 = []
opq_Set = [[i,i+1] for i in range(n-1)]
opq_Set.append([0,6])
prob = [float(1-q)/n for i in range(n)]
opq_prob = [q/n for i in range(n)]

for S in Slist:
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    scenario4.append(cost(n,h,K,lamb, S, ER,ER2))

benchmark = []
q = 0
opq_Set = [[0,1,2,3,4,5,6]]
prob = [float(1-q)/n for i in range(n)]
opq_prob = [q]
for S in Slist:
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set, S, iteration)
    benchmark.append(cost(n,h,K,lamb, S, ER,ER2))

######################################################################
# plot holding cost
t = Slist
d1 = [100*(1-scenario3[i][1]/benchmark[i][1]) for i in range(len(benchmark))]
d2 = [100*(1-scenario2[i][1]/benchmark[i][1]) for i in range(len(benchmark))]
d3 = [100*(1-scenario1[i][1]/benchmark[i][1]) for i in range(len(benchmark))]
d4 = [100*(1-scenario4[i][1]/benchmark[i][1]) for i in range(len(benchmark))]
fig = plt.figure(figsize=(12, 5))
ax = plt.subplot(1, 2, 1)
y=plt.plot(t2,d1, 'or-',t2,d2,'sb-',t2,d3, '^g-', t2, d4, '*c-')
plt.ylabel('Holding Cost Savings (%)', fontsize = 14)
plt.xlabel('$S$', fontsize = 14)
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylim(0,9)

######################################################################
# ordering cost
d1 = [100*(1-scenario3[i][2]/benchmark[i][2]) for i in range(len(benchmark))]
d2 = [100*(1-scenario2[i][2]/benchmark[i][2]) for i in range(len(benchmark))]
d3 = [100*(1-scenario1[i][2]/benchmark[i][2]) for i in range(len(benchmark))]
d4 = [100*(1-scenario4[i][2]/benchmark[i][2]) for i in range(len(benchmark))]
ax = plt.subplot(1, 2, 2)
y=plt.plot(t2,d1, 'or-',t2,d2,'sb-',t2,d3, '^g-', t2, d4, '*c-')
plt.ylabel('Ordering Cost Savings (%)', fontsize = 14)
plt.xlabel('$S$', fontsize = 14)
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.legend(y,['n-opq','categorical $w=3/7$','categorical $w=1/7$', 'circle'],loc='best', fontsize=14,shadow=True, fancybox=True)
plt.ylim(0,12)
plt.show()
fig.savefig('general_model_S_2.pdf',bbox_inches='tight') 

