#How to check if there's a node or a subgraph isolated?

from random import randrange
import numpy as np
link_prob = 5 # 0.5 prob for each link
print("substrate network for InP1")
node_num_1 = randrange(5)+1
node1_cap = np.zeros(node_num_1)
print(node_num_1) 
for i in range (node_num_1):
    node1_cap[i] = randrange(10)+1 # CPU of substrate nodes
print(node1_cap)

link_1 = np.zeros((node_num_1, node_num_1))
for i in range(node_num_1):
    for j in range(i+1,node_num_1):
        link_1[i][j] = randrange(10) #decide connectivty
        
        if link_1[i][j]>link_prob:
            link_1[i][j] = randrange(10)+1 #decide bandwidth            
        else:
            link_1[i][j] = 0
        link_1[j][i] = link_1[i][j]
print(link_1)

#check whether there's a node connecting with no other nodes
#print(link.sum(1))
for i in link_1.sum(1):
    if i ==  0:
        print("generate again please!")
        break
        
        
        
print("substrate network for InP2")
node_num_2 = randrange(5)+1
node2_cap = np.zeros(node_num_2)
print(node_num_2) # number of substrate nodes
for i in range (node_num_2):
    node2_cap[i] = randrange(10)+1 # CPU capacity
print(node2_cap) 
link_2 = np.zeros((node_num_2, node_num_2))
for i in range(node_num_2):
    for j in range(i+1,node_num_2):
        link_2[i][j] = randrange(10) #decide connectivty
        
        if link_2[i][j]>link_prob:
            link_2[i][j] = randrange(10)+1 #decide bandwidth id two nodes are connected            
        else:
            link_2[i][j] = 0
        link_2[j][i] = link_2[i][j]
print(link_2)

#check whether there's a node connecting with no other nodes
#print(link.sum(1))
for i in link_2.sum(1):
    if i ==  0:
        print("generate again please!")
        break
        
# connect two substrate network
# set bandwidth of inter-connected links to be 100
link = np.zeros((node_num_1 + node_num_2, node_num_1 + node_num_2))
bw_inter = 100
for i in range(node_num_1 + node_num_2):
    for j in range(i, node_num_1 + node_num_2):
        if i<node_num_1 and j<node_num_1:
            link[i][j] = link_1[i][j]
        elif i<node_num_1 and j>=node_num_1:
            link[i][j] = randrange(10)
            if link[i][j]> 5:
                link[i][j] = bw_inter
            else:
                link[i][j] = 0
        if i>=node_num_1 and j>=node_num_1:
            link[i][j] = link_2[i-node_num_1][j-node_num_1]
        
        link[j][i] = link[i][j]
print(link)


# wirte into file
fp = open("substrate1123.txt", "a")
fp.write(str(int(node_num_1))+'\n')

fp.write(str(int(node_num_2))+'\n')

for i in range(node_num_1):
    fp.write(str(int(node1_cap[i])))
    fp.write(' ')
fp.write('\n')
for i in range(node_num_2):
    fp.write(str(int(node2_cap[i])))
    fp.write(' ')
fp.write('\n')

for i in range(node_num_1 + node_num_2):
    for j in range(node_num_1 + node_num_2):        
        fp.write(str(int(link[i][j])))
        fp.write(' ')
    fp.write('\n')
        #fp.write(str(link[j][0])+'\n')
fp.close()
