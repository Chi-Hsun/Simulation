import pandas as pd
import numpy as np
filename = 'substrate1123.txt'

def read_substrate(filename):
    with open(filename, 'r') as f:#with語句自動呼叫close()方法
        Inp1_nodenum = int(f.readline())
        Inp2_nodenum = int(f.readline())
        link = np.zeros((Inp1_nodenum+Inp2_nodenum,Inp1_nodenum+Inp2_nodenum))
        CPU = np.zeros(Inp1_nodenum+Inp2_nodenum)
        
        for i in range(2):
            line = f.readline()
            temp = line.split()
            for j in range(len(temp)):
                CPU[i*len(temp)+j] = int(temp[j])
        for i in range(Inp1_nodenum+Inp2_nodenum):
            line = f.readline()
            link[i] = line.split()
            
    return CPU,link

cpu, link = read_substrate(filename)


filename = 'virtual1123.txt'
def read_virtual(filename):
    VNR_list = np.genfromtxt(filename)
    VNR_list = list(VNR_list)
    return VNR_list
VNR_list = read_virtual(filename)
print(VNR_list)
