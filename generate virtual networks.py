# virtual network
#line topology

from random import randrange
import numpy as np

fp = open("virtual1123.txt", "a")

timeslots = 30
arrtime = 0
for i in range(timeslots):
    num_of_arrivals = np.random.poisson(0.5)  #number of arrivals in this timeslot
    print( "num of arrivals in", i, "timeslot: ", num_of_arrivals)
    for f in range(num_of_arrivals):
        fp.write(str(int(arrtime))+'\n')
        print(arrtime)
   
        lifetime = np.random.poisson(20)  #lifetime
        fp.write(str(int(lifetime))+'\n')
        print(lifetime)
                
        node_num = randrange(2,5)+1    # node num
        fp.write(str(int(node_num))+'\n')
        print(node_num)
    
        for j in range (node_num):
            node_cap = randrange(5)+1   #CPU requirement
            fp.write(str(int(node_cap))+'\n')
            print(node_cap)
        for k in range(node_num-1):
            bw = randrange(5)+1   #BW requirement
            fp.write(str(int(bw))+'\n')
            print(bw)
    arrtime = arrtime + 1
fp.close()
