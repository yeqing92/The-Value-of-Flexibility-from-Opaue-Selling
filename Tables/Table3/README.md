Table 3 contains numerical results with backlogging costs, lost sales costs, and lead time.

We conduct a grid search for each set of parameters.

 - The code that generates the data file can be found in nopq_backorderandlostsales.py
   function createDemand, createChoice, and createOpaque create the arrival time, choice, and whether flexible or not for each customer
   
 - The code that generates the two choice for 2 opaque product can be found in 2opq_noleadtime.py
   function createTwoChoice creates the two products that a flexible customer is willing to choose

The files that generate results:
- 2opq_noleadtime.py generates results for 2 opaque selling with lead time = 0 and no backordering or lost sales costs
- 2opq_backorder.py generates results for 2 opaque selling with backordering costs and positive lead time
- 2opq_lostsales.py generates results for 2 opaque selling with lost sales costs and positive lead time
- nopq_noleadtime.py generates results for n opaque selling with lead time = 0 and no backordering or lost sales costs
- nopq_backorderandlostsales.py generates results for n opaque selling with positive lead time, using different functions for backordering costs and lost sales costs.
