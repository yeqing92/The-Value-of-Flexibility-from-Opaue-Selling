#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from itertools import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import json      

# balancing onhand inventory
def backorderCost2OPQ(s, S, N, K, h,L, q, lamb ,b , iteration):
    Total_holding = 0
    Total_ordering = 0
    Total_back = 0
    Time = 0
    onhand = [0 for i in range(N)]
    inv_position = [S for i in range(N)]
    pipeline = [(0,[S for i in range(N)] )]
    txtname1 = "may31interArrivalTime_" + "_"+str(lamb)+".txt"
    txtname2 = "may31choice" + "_"+str(N)+".txt"
    txtname2OPQ = "june7_2choice" + "_"+str(N)+".txt"
    txtname3 = "may31opaque" + "_"+str(q)+".txt"

    with open(txtname1, 'r') as in_file:
        time = json.load(in_file)

    with open(txtname2, 'r') as in_file:
        choice = json.load(in_file)
    
    with open(txtname3, 'r') as in_file:
        opaque = json.load(in_file)
        
    with open(txtname2OPQ, 'r') as in_file:
        twoChoice = json.load(in_file)
        
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
        
        
        if (opaque[i]==0):
            customer = choice[i]
        else:
            if (onhand[twoChoice[i][0]] > onhand[twoChoice[i][1]]):
                customer = twoChoice[i][0]
            else:
                customer = twoChoice[i][1]   
        onhand[customer]= onhand[customer] - 1
        inv_position[customer] = inv_position[customer] - 1
        back_indicator =[-(onhand[i] < 0 ) for i in range(N)]
        if (np.min(inv_position)<=s):
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
             result[s,S] = backorderCost2OPQ(s, S, N, K, h, L , 0.1, lamb ,b, iteration)
    print("!!!0.1 done!!!")

    result2 = dict()
    result2 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
             result2[s,S] = backorderCost2OPQ(s, S, N, K, h, L , 0.2, lamb ,b, iteration)
    print("!!!0.2 done!!!")

    result0 = dict()

    result0 = {(s,S):0 for s in sRange for S in SRange}
    for S in SRange:
        print(S)
        for s in sRange:
            result0[s,S] = backorderCost2OPQ(s, S, N, K, h, L , 0, lamb ,b, iteration)
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


#############################################################
sRange = list(range(-5,0))
SRange =  list(range(7, 12))
L = 1
b = 10  # back order cost
iteration = 1000000
# possible policy (-3,9)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)
#############################################################
sRange = list(range(-1,4))
SRange =  list(range(12, 17))
L = 2
b = 10  # back order cost
iteration = 1000000
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)
#############################################################
sRange = list(range(1,9))
SRange =  list(range(12,26))
L = 3
b = 10  # back order cost
iteration = 1000000
# possible policy (5,18)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)
#############################################################
sRange = list(range(-2,3))
SRange =  list(range(9, 14))
L = 1
b = 30  # back order cost
iteration = 1000000
# possible policy (0,11)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)
#############################################################
sRange = list(range(2,7))
SRange =  list(range(13, 19))
L = 2
b = 30  # back order cost
iteration = 1000000
# possible policy(4,16)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)
#############################################################
sRange = list(range(5,12))
SRange =  list(range(14, 26))
L = 3
b = 30  # back order cost
iteration = 1000000
# possible policy (9,20)
run_balance_onhand_backlog(b ,L,  iteration, sRange,SRange)

