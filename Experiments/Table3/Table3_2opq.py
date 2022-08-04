#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from itertools import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import json   
# Given s and S, compute the cost

def lost_2OPQ_sub(s, S, N, K, h,L, q, lamb ,l, iteration):
    Total_holding = 0
    Total_ordering = 0
    Total_lost = 0
    Time = 0
    onhand = [0 for i in range(N)]
    inv_position = [S for i in range(N)]
    pipeline= [(0,[S for i in range(N)])]
    
    txtname1 = "may31interArrivalTime_" + "_"+str(lamb)+".txt"
    txtname2 = "may31choice" + "_"+str(N)+".txt"
    txtname3 = "may31opaque" + "_"+str(q)+".txt"
    txtname2OPQ = "june7_2choice" + "_"+str(N)+".txt"

    with open(txtname1, 'r') as in_file:
        time = json.load(in_file)
    with open(txtname2, 'r') as in_file:
        choice = json.load(in_file)
    with open(txtname3, 'r') as in_file:
        opaque = json.load(in_file)
    with open(txtname2OPQ, 'r') as in_file:
        twoChoice = json.load(in_file)

    for i in range(iteration-1):   
        if (len(pipeline)>=1):
            next_time = pipeline[0][0] # next order arrival time
            order = pipeline[0][1]
        else:
            next_time = 0
            
        if (next_time >= Time) and (next_time < Time + time[i+1] ):
            Total_ordering = Total_ordering + K
            # replenished
            Total_holding = Total_holding + h * (next_time - Time) * sum([onhand[i] for i in range(len(onhand) ) if onhand[i]>0] )
            onhand = [onhand[i] + order[i] for i in range(N)]
            pipeline = pipeline[1:]

            Total_holding = Total_holding + h* ( Time + time[i+1] - next_time) * sum([onhand[i] for i in range(len(onhand) ) if onhand[i]>0] )
        else:
            Total_holding = Total_holding + h * time[i+1] * sum([onhand[i] for i in range(len(onhand) ) if onhand[i]>0] )
        
        Time = Time + time[i+1]
        
        
        customer = choice[i]
        if onhand[choice[i]]<=0 and (opaque[i]==1):
            temp = [twoChoice[i][k] for k in range(2) if onhand[twoChoice[i][k] ] >0]
            if len(temp)>0:
                customer = temp[0]
                
#             if (onhand[twoChoice[i][0] ] > onhand[twoChoice[i][1]]):
#                 customer = twoChoice[i][0]
#             else:
#                 customer = twoChoice[i][1]
        if (onhand[customer] > 0): 
            onhand[customer]= onhand[customer] - 1
            inv_position[customer]= inv_position[customer] - 1
        else:
            Total_lost = Total_lost + l 
        
        if (np.min(inv_position)<=s):
            re_time = Time + L
            re = [S-inv_position[i] for i in range(N)]
            pipeline.append((re_time, re))
            inv_position = [S for i in range(N)]

            
    average = Total_holding/iteration + Total_ordering/iteration + Total_lost/iteration
#     print( Total_ordering)
#     print(Total_holding)
#     print(Total_lost)
    return average

def run_lostsale_sub(l,L, iteration, sRange,SRange):
    N = 5
    K = 150
    h = 6
    lamb = 0.05 # 20 customers per day
    result = dict()
    result = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result[s,S] =lost_2OPQ_sub(s, S, N, K, h,L, 0.1, lamb ,l, iteration)
    print("!!!0.1 done!!!")

    result2 = dict()
    result2 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result2[s,S] =lost_2OPQ_sub(s, S, N, K, h,L, 0.2, lamb ,l, iteration)
    print("!!!0.2 done!!!")
    
    result0 = dict()
    result0 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
            result0[s,S] = lostCost2OPQ(s, S, N, K, h,L, 0, lamb ,l, iteration)
    #         result0[s,S] = test_lostCost(s, S, N, K, h, L , 0, lamb ,l, iteration)
    
    print("Result for q = 0.1")
    min_q = min(result.values())
    print(min_q )
    policy_q = min(result, key=lambda k: result[k])
    print(policy_q)
    min_0 = min(result0.values())
    print(min_0 )
    index = min(result0, key=lambda k: result0[k])
    print(index)
    print(result[index])
    improvement_1 = 100*(min_0 - min_q)/min_0
    improvement_2 = 100*(min_0 - result[index])/min_0
    print(improvement_1)
    print(improvement_2)
    
    
    print("Result for q = 0.2")
    min_q = min(result2.values())
    print(min_q )
    policy_q = min(result2, key=lambda k: result2[k])
    print(policy_q)
    min_0 = min(result0.values())
    print(min_0 )
    index = min(result0, key=lambda k: result0[k])
    print(index)
    print(result2[index])
    improvement_1 = 100*(min_0 - min_q)/min_0
    improvement_2 = 100*(min_0 - result2[index])/min_0
    print(improvement_1)
    print(improvement_2)
    print(result)
    print(result2)
    print(result0)

#############################################
"""lost sales"""

sRange = list(range(1,4))
SRange =  list(range(10, 17))
L = 1
l = 30
iteration = 1000000
run_lostsale_sub(l,L, iteration, sRange,SRange)
#############################################

sRange = list(range(4,9))
SRange =  list(range(14, 19))
L = 2
l = 30
iteration = 1000000
run_lostsale_sub(l,L, iteration, sRange,SRange)

#############################################
sRange = list(range(5,15))
SRange =  list(range(15, 25))
L = 3
l = 30
iteration = 1000000
run_lostsale_sub(l,L, iteration, sRange,SRange)

#############################################

sRange = list(range(0,8))
SRange =  list(range(10, 19))
L = 1
l = 50
iteration = 1000000
run_lostsale_sub(l,L, iteration, sRange,SRange)

#############################################

sRange = list(range(5,10))
SRange =  list(range(15, 20))
L = 2
l = 50
iteration = 1000000
run_lostsale_sub(l,L, iteration, sRange,SRange)

#############################################
sRange = list(range(9,16))
SRange =  list(range(19, 26))
L = 3
l = 50
iteration = 1000000
run_lostsale_sub(l,L, iteration, sRange,SRange)

