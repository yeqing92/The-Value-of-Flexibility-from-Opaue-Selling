#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from itertools import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import json

# Generate demand and save to file
def createDemand(lamb, iteration):
    txtname = "may31interArrivalTime_" + "_"+str(lamb)+".txt"
    time = np.random.exponential(scale = lamb,  size = iteration) 
    demand = [time[i] for i in range(len(time))]
#     print(np.mean(demand))
    with open(txtname, 'w') as out_file:
        json.dump(demand, out_file)
        
def createChoice(N, iteration):
    txtname = "may31choice" + "_"+str(N)+".txt"
    sample = np.random.randint(0,N,iteration)
    choice = [int(sample[i]) for i in range(len(sample))]
#     print(np.sum([choice[i]==4 for i in range(len(choice))]))    
    with open(txtname, 'w') as out_file:
        json.dump(choice, out_file)

def createOpaque(q, iteration):
    txtname = "may31opaque" + "_"+str(q)+".txt"
    sample = np.random.binomial(1, q, iteration)
    choice = [int(sample[i]) for i in range(len(sample))]
    with open(txtname, 'w') as out_file:
        json.dump(choice, out_file)
    print(sum(sample))
########################################################## 
# use this block to create customer choice files
# N = 5
# K = 150
# h = 6
# L = 2
# lamb = 0.05 # 20 customers per day
# l = 30  # lost sale penalty
# iteration = 1000000

# createOpaque(0, iteration)
# createOpaque(0.1, iteration)
# createOpaque(0.2, iteration)
########################################################

# balancing onhand inventory
def backorderCost(s, S, N, K, h,L, q, lamb ,b , iteration):
    Total_holding = 0
    Total_ordering = 0
    Total_back = 0
    Time = 0
    onhand = [0 for i in range(N)]
    inv_position = [S for i in range(N)]
    pipeline = [(0,[S for i in range(N)] )]
    txtname1 = "may31interArrivalTime_" + "_"+str(lamb)+".txt"
    txtname2 = "may31choice" + "_"+str(N)+".txt"
    txtname3 = "may31opaque" + "_"+str(q)+".txt"
    with open(txtname1, 'r') as in_file:
        time = json.load(in_file)

    with open(txtname2, 'r') as in_file:
        choice = json.load(in_file)
    
    with open(txtname3, 'r') as in_file:
        opaque = json.load(in_file)
        
    back_indicator = [0 for i in range(N)]
    order_indicator = 1
    replenish_time = [0]
    for i in range(iteration-1):    
        if (len(pipeline)>= 1):
            next_time = pipeline[0][0]
            income_order = pipeline[0][1]
        else:
            next_time =0
        
        if (next_time >= Time) and (next_time < Time + time[i+1] ):
            Total_ordering = Total_ordering + K
            # replenished
            Total_holding = Total_holding + h * (next_time - Time) * sum([onhand[i] for i in range(len(onhand) ) if onhand[i]>0] )
            Total_back = Total_back + b * (next_time - Time) * sum( [onhand[i] * back_indicator[i] for i in range(N)])
            onhand = [onhand[i] + income_order[i] for i in range(N)]
            back_indocator = [-(onhand[i] < 0 ) for i in range(N)]
            Total_holding = Total_holding + h* ( Time + time[i+1] - next_time) * sum([onhand[i] for i in range(len(onhand) ) if onhand[i]>0] )
            Total_back = Total_back + b * (Time + time[i+1] - next_time) * sum( [onhand[i] * back_indicator[i] for i in range(N)])

            pipeline = pipeline[1:]
            
        else:
            Total_holding = Total_holding + h * time[i+1] * sum([onhand[i] for i in range(len(onhand) ) if onhand[i]>0] )
            Total_back = Total_back + b *time[i+1]* sum( [onhand[i] * back_indicator[i] for i in range(N)])

        Time = Time + time[i+1]
        
        customer = choice[i] * (opaque[i] == 0 ) + np.argmax(onhand) * (opaque[i] == 1)
        onhand[customer]= onhand[customer] - 1
        inv_position[customer] = inv_position[customer] - 1
        back_indicator =[-(onhand[i] < 0 ) for i in range(N)]
        

        if (np.min(inv_position)<=s):
#             order_indicator = 1
            replenish_time = Time + L
            replenish = [S-inv_position[i] for i in range(N)]
            pipeline.append((replenish_time, replenish))
            inv_position = [S for i in range(N)]

            
    average = Total_holding/iteration + Total_ordering/iteration + Total_back/iteration
    return average

def run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange):
    h = 6
    N = 5
    lamb = 0.05 # 20 customers per day
    K = 150
    
    result = dict()
    result = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result[s,S] = backorderCost(s, S, N, K, h, L , 0.1, lamb ,b, iteration)
    print("!!!0.1 done!!!")

    result2 = dict()
    result2 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result2[s,S] = backorderCost(s, S, N, K, h, L , 0.2, lamb ,b, iteration)
    print("!!!0.2 done!!!")

    result0 = dict()

    result0 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
            result0[s,S] = backorderCost(s, S, N, K, h, L , 0, lamb ,b, iteration)
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
    
#########################################################
# Given s and S, compute the cost
# Lost Sales for n-opaque
def lostCost(s, S, N, K, h,L, q, lamb ,l, iteration):
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
    with open(txtname1, 'r') as in_file:
        time = json.load(in_file)
    with open(txtname2, 'r') as in_file:
        choice = json.load(in_file)
    with open(txtname3, 'r') as in_file:
        opaque = json.load(in_file)
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
        
        customer = choice[i] * (opaque[i] == 0 ) + np.argmax(onhand) * (opaque[i] == 1)
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
    return average

def run_lostsale(l,L, iteration, sRange,SRange):
    N = 5
    K = 150
    h = 6
    lamb = 0.05 # 20 customers per day
    result = dict()
    result = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result[s,S] =lostCost(s, S, N, K, h,L, 0.1, lamb ,l, iteration)
    print("!!!0.1 done!!!")

    result2 = dict()
    result2 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result2[s,S] =lostCost(s, S, N, K, h,L, 0.2, lamb ,l, iteration)
    print("!!!0.2 done!!!")
    
    result0 = dict()
    result0 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
            result0[s,S] = lostCost(s, S, N, K, h,L, 0, lamb ,l, iteration)
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

################################
"""lost sale"""
##################################################################

sRange = list(range(0,9))
SRange =  list(range(9, 19))
L = 1
l = 30
iteration = 1000000
# policy (2,12)
run_lostsale(l,L, iteration, sRange,SRange)

##################################################################

sRange = list(range(4,10))
SRange =  list(range(14, 19))
L = 2
l = 30
iteration = 1000000
# policy (6,16)
run_lostsale(l,L, iteration, sRange,SRange)

##################################################################

sRange = list(range(4,15))
SRange =  list(range(15, 25))
L = 3
l = 30
iteration = 1000000
# policy (9,19)
run_lostsale(l,L, iteration, sRange,SRange)

##################################################################

sRange = list(range(0,6))
SRange =  list(range(10, 19))
L = 1
l = 50
iteration = 1000000
# possible policy (3,13)
run_lostsale(l,L, iteration, sRange,SRange)

##################################################################
sRange = list(range(2,10))
SRange =  list(range(11, 21))
L = 2
l = 50
iteration = 1000000
# policy (6, 16)
run_lostsale(l,L, iteration, sRange,SRange)
##################################################################
sRange = list(range(5,15))
SRange =  list(range(15, 25))
L = 3
l = 50
iteration = 1000000
# policy (11,21)
run_lostsale(l,L, iteration, sRange,SRange)

##################################################################
"""backorder"""

sRange = list(range(-5,0))
SRange =  list(range(7, 12))
L = 1
b = 10  # back order cost
iteration = 1000000
# possible policy (-3,9)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)

##################################################################

sRange = list(range(-2,4))
SRange =  list(range(11, 17))

L = 2
b = 10  # back order cost
iteration = 1000000
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)

##################################################################
sRange = list(range(2,9))
SRange =  list(range(16,28))

L = 3
b = 10  # back order cost
iteration = 1000000
# policy (5,18)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)

#####################################################################################

sRange = list(range(-2,2))
SRange =  list(range(8, 13))

L = 1
b = 30  # back order cost
iteration = 1000000
# possible policy (0,11)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)
#################################################################
sRange = list(range(2,7))
SRange =  list(range(13, 19))
L = 2
b = 30  # back order cost
iteration = 1000000
# possible policy(4,16)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)

##################################################################
sRange = list(range(6,11))
SRange =  list(range(18, 23))

L = 3
# q = 0.2
b = 30  # back order cost
# iteration = 1000000
iteration = 30000
# possible policy (8,20)

run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)

##################################################################

