from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import random
import math
import csv
from collections import Counter
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
S = 50
q=0.3
qminlist = []
result = []

for t in range(1000):
    print(t)
    opq_Set = [list(range(n))]
    opq_prob = [q]
    temp = [random.randint(1,10) for i in range(n)]
    prob = [float(1)/n - q*float(temp[i])/sum(temp) for i in range(n)]
    min_qi = min([q*float(temp[i])/sum(temp)*n  for i in range(n) ])
    qminlist.append(min_qi)
    [ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set,S, 10000)
    result.append(cost(n,h,K,lamb, S, ER,ER2)[0])

# traditional selling, no opaque
q=0
prob = [float(1-q)/n for i in range(n)]
opq_Set = [[i for i in range(n)]]
opq_prob = [q]
[ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set,S, 10000)
baseline1 = cost(n,h,K,lamb, S, ER,ER2)

# symmetric, n opaque product
q = 0.3
prob = [float(1-q)/n for i in range(n)]
opq_Set = [[i for i in range(n)]]
opq_prob = [q]
# prob = [] # asymmetric
[ER, ER2] = simulate_ER(n,prob, opq_prob, opq_Set,S, 10000)
print(ER)
print(ER2)
baseline2 = cost(n,h,K,lamb, S, ER,ER2)

############################################################################
# plot figure 3
fig = plt.figure(figsize=(6, 5))
ax = plt.subplot(1, 1, 1)
y=plt.plot(qminlist, [100*(1-i/baseline1[0]) for i in result], '*')
plt.axhline(y=100*(1-baseline2[0]/baseline1[0]),color='k', linestyle='--')
plt.ylabel('Relative Cost Savings (%)', fontsize = 14)
plt.xlabel('$q_{min}$', fontsize = 14)
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylim(3,11)
plt.show()
fig.savefig('q_min.pdf',bbox_inches='tight')

