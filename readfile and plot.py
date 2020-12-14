

import matplotlib.pyplot as plt
import numpy as np
filename = 'result1212-2.txt'
with open(filename, 'r') as f:
    revenue = f.readline()
    cost = f.readline()
    acc = f.readline()
    RC = f.readline()
    cpu_uti = f.readline()
    bw_uti = f.readline()
revenue = revenue[11:-2]
print(revenue)
revenue = revenue.translate({ord(','): None}) #remove the comma
revenue = revenue.split()
revenue = [ int(float(x)) for x in revenue] # convert string to int
cost = cost[8:-2]
cost = cost.translate({ord(','): None})
cost = cost.split()
cost = [ int(float(x)) for x in cost]
acc = acc[20:-2]
acc = acc.translate({ord(','): None})
acc = acc.split()
acc = [ float(x) for x in acc] #convert string to float
RC = RC[13:-2]
RC = RC.translate({ord(','): None})
RC = RC.split()
RC = [ float(x) for x in RC]

cpu_uti = cpu_uti[19:-2]
cpu_uti = cpu_uti.translate({ord(','): None})
cpu_uti = cpu_uti.split()
cpu_uti = [ float(x) for x in cpu_uti]

bw_uti = bw_uti[18:-2]
bw_uti = bw_uti.translate({ord(','): None})
bw_uti = bw_uti.split()
bw_uti = [ float(x) for x in bw_uti]



%matplotlib inline
ironman = np.linspace(0,1000,1000)
fig = plt.figure() #定義一個圖像窗口
plt.plot(ironman, revenue, '.') #定義x,y和圖的樣式
plt.title('revenue comparison')
plt.xlabel('timeslot')  
plt.ylabel('revenue') 
plt.savefig('revenue.png')


%matplotlib inline
ironman = np.linspace(0,1000,1000)
fig = plt.figure() #定義一個圖像窗口
plt.plot(ironman, cost, '.') #定義x,y和圖的樣式
plt.title('cost comparison')
plt.xlabel('timeslot')  
plt.ylabel('cost') 
plt.savefig('cost.png')

%matplotlib inline
ironman = np.linspace(0,1000,1000)
fig = plt.figure() #定義一個圖像窗口
plt.plot(ironman, acc, '.') #定義x,y和圖的樣式
plt.title('acceptance ratio comparison')
plt.ylim((0,1.1))
plt.xlabel('timeslot')  
plt.ylabel('acceptance ratio') 
plt.savefig('acceptance ratio.png')




%matplotlib inline
ironman = np.linspace(0,1000,1000)
fig = plt.figure() #定義一個圖像窗口
plt.plot(ironman, RC, '.') #定義x,y和圖的樣式
plt.ylim((0,1.1))
plt.title('RC ratio comparison')
plt.xlabel('timeslot')  
plt.ylabel('RC ratio') 
plt.savefig('RC.png')



%matplotlib inline
ironman = np.linspace(0,1000,1000)
fig = plt.figure() #定義一個圖像窗口
plt.plot(ironman, cpu_uti, '.') #定義x,y和圖的樣式
plt.ylim((0,1))
plt.title('CPU utilization')
plt.xlabel('timeslot')  
plt.ylabel('CPU utilization') 
plt.savefig('CPU utilization.png')



%matplotlib inline
ironman = np.linspace(0,1000,1000)
fig = plt.figure() #定義一個圖像窗口
plt.plot(ironman, bw_uti, '.') #定義x,y和圖的樣式
plt.ylim((0,1))
plt.title('BW utilization')
plt.xlabel('timeslot')  
plt.ylabel('BW utilization') 
plt.savefig('BW utilization.png')
